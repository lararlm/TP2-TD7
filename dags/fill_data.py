from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.taskinstance import TaskInstance
import pendulum
import sys
import os

# Adds the parent directory to the Python path to find the 'td7' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from td7.data_generator import DataGenerator
from td7.schema import Schema

# --- Constants ---
PEOPLE_TO_GENERATE = 200
UNITS_TO_GENERATE = 5
SPACES_TO_GENERATE = 10

# =============================================================================
# DEFINE PYTHON CALLABLES FOR EACH TASK
# =============================================================================

# --- Functions for People & Complaints Path ---

def _generate_people(n: int):
    """Wipes and inserts the core people entities."""
    schema = Schema()
    print("Truncating people-related tables...")
    schema.truncate_table("Persona")

    print(f"Generating {n} base people entities.")
    generator = DataGenerator()
    personas = generator.generate_personas(n=n)
    schema.insert(personas, "Persona")
    solicitantes = generator.generate_solicitantes(personas)
    schema.insert(solicitantes, "Solicitante")
    denunciados = generator.generate_denunciados(personas)
    schema.insert(denunciados, "Denunciado")
    print("People entities inserted successfully.")
    # Return the generated data for the downstream task
    return {
        "personas": personas,
        "solicitantes": solicitantes,
        "denunciados": denunciados
    }

def _link_complaints(ti: TaskInstance):
    """Wipes and inserts the 'denuncias', linking people from the previous task."""
    schema = Schema()
    print("Truncating complaint links table...")
    schema.truncate_table("Denuncia")

    print("Generating complaint links (denuncias).")
    # Pull the generated people data from the upstream task
    data = ti.xcom_pull(task_ids='generate_people')
    solicitantes = data["solicitantes"]
    denunciados = data["denunciados"]

    generator = DataGenerator()
    denuncias = generator.generate_denuncias(solicitantes, denunciados)
    schema.insert(denuncias, "Denuncia")
    print("Complaint links inserted successfully.")


# --- Functions for Spaces & Incidents Path ---

def _generate_and_classify_spaces():
    """Generates Unidades and Espacios, then classifies them for parallel processing."""
    schema = Schema()
    generator = DataGenerator()

    print("Truncating structure-related tables...")
    schema.truncate_table("Unidad")
    schema.truncate_table("Espacio")
    schema.truncate_table("Suceso") # Truncate Suceso here as well

    print("Generating Unidades and base Espacios...")
    unidades = generator.generate_unidades(n=UNITS_TO_GENERATE)
    schema.insert(unidades, "Unidad")
    
    espacios, academicos, no_academicos = generator.generate_espacios(n=SPACES_TO_GENERATE)
    schema.insert(espacios, "Espacio")
    
    print(f"Classified {len(academicos)} academic spaces and {len(no_academicos)} non-academic spaces.")
    
    # Pass data to downstream tasks via XComs
    return {
        "unidades": unidades,
        "espacios": espacios,
        "academicos": academicos,
        "no_academicos": no_academicos
    }

def _process_academic_spaces(ti: TaskInstance):
    """Processes the list of academic spaces."""
    data = ti.xcom_pull(task_ids='generate_and_classify_spaces')
    academicos = data["academicos"]
    unidades = data["unidades"]

    if not academicos:
        print("No academic spaces to process.")
        return

    print(f"Processing {len(academicos)} academic spaces...")
    schema = Schema()
    generator = DataGenerator()

    espacios_academicos = generator.generate_espacio_academico(academicos, unidades)
    schema.insert(espacios_academicos, "Espacio_Academico")
    unidades_pertenencia = generator.generate_unidad_pertenencia(unidades)
    schema.insert(unidades_pertenencia, "Unidad_Pertenece_A")
    print("Academic spaces processed successfully.")

def _process_non_academic_spaces(ti: TaskInstance):
    """Processes the list of non-academic spaces."""
    data = ti.xcom_pull(task_ids='generate_and_classify_spaces')
    no_academicos = data["no_academicos"]

    if not no_academicos:
        print("No non-academic spaces to process.")
        return
        
    print(f"Processing {len(no_academicos)} non-academic spaces...")
    schema = Schema()
    generator = DataGenerator()

    espacios_no_academicos = generator.generate_espacio_no_academico(no_academicos)
    schema.insert(espacios_no_academicos, "Espacio_No_Academico")
    print("Non-academic spaces processed successfully.")

def _generate_incidents(ti: TaskInstance):
    """Generates incidents related to all spaces."""
    data = ti.xcom_pull(task_ids='generate_and_classify_spaces')
    espacios = data["espacios"]

    if not espacios:
        print("No spaces found to generate incidents for.")
        return

    print(f"Generating incidents for {len(espacios)} spaces...")
    schema = Schema()
    generator = DataGenerator()

    sucesos = generator.generate_sucesos(espacios)
    schema.insert(sucesos, "Suceso")
    print("Incidents generated successfully.")

# =============================================================================
# DEFINE THE AIRFLOW DAG
# =============================================================================

with DAG(
    dag_id="full_data_pipeline_with_bifurcation",
    start_date=pendulum.datetime(2025, 6, 22, tz="UTC"),
    schedule_interval="@daily",
    catchup=False,
    description="Generates all data with a bifurcation for space processing."
) as dag:
    
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # --- Path A: People & Complaints Tasks ---
    generate_people_task = PythonOperator(
        task_id="generate_people",
        python_callable=_generate_people,
        op_kwargs={"n": PEOPLE_TO_GENERATE},
    )

    link_complaints_task = PythonOperator(
        task_id="link_complaints",
        python_callable=_link_complaints,
    )

    # --- Path B: Spaces & Incidents Tasks ---
    generate_and_classify_spaces_task = PythonOperator(
        task_id="generate_and_classify_spaces",
        python_callable=_generate_and_classify_spaces,
    )

    process_academic_spaces_task = PythonOperator(
        task_id="process_academic_spaces",
        python_callable=_process_academic_spaces,
    )

    process_non_academic_spaces_task = PythonOperator(
        task_id="process_non_academic_spaces",
        python_callable=_process_non_academic_spaces,
    )

    generate_incidents_task = PythonOperator(
        task_id="generate_incidents",
        python_callable=_generate_incidents,
    )

    # --- Define Final Workflow Dependencies ---
    start >> [generate_people_task, generate_and_classify_spaces_task]
    
    generate_people_task >> link_complaints_task
    
    generate_and_classify_spaces_task >> [process_academic_spaces_task, process_non_academic_spaces_task]
    [process_academic_spaces_task, process_non_academic_spaces_task] >> generate_incidents_task
    
    [link_complaints_task, generate_incidents_task] >> end