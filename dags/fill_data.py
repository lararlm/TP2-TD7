from airflow import DAG
from airflow.operators.python import PythonOperator
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

def _generate_people(n: int):
    """
    Task 1: Wipes and inserts the core people entities.
    """
    schema = Schema()
    # === IDEMPOTENCY FIX: Truncate tables first ===
    print("Truncating people-related tables...")
    schema.truncate_table("Persona") # This will also truncate Solicitante and Denunciado via CASCADE

    print(f"Generating {n} base people entities.")
    generator = DataGenerator()
    personas = generator.generate_personas(n=n)
    schema.insert(personas, "Persona")
    solicitantes = generator.generate_solicitantes(personas)
    schema.insert(solicitantes, "Solicitante")
    denunciados = generator.generate_denunciados(personas)
    schema.insert(denunciados, "Denunciado")
    print("People entities inserted successfully.")

def _generate_university_structure(num_units: int, num_spaces: int):
    """
    Task 2: Wipes and inserts the university's structure.
    """
    schema = Schema()
    # === IDEMPOTENCY FIX: Truncate tables first ===
    print("Truncating structure-related tables...")
    schema.truncate_table("Unidad")
    schema.truncate_table("Espacio")

    print("Generating university structure (units and spaces).")
    generator = DataGenerator()
    unidades = generator.generate_unidades(n=num_units)
    schema.insert(unidades, "Unidad")
    unidades_pertenencia = generator.generate_unidad_pertenencia(unidades)
    schema.insert(unidades_pertenencia, "Unidad_Pertenece_A")
    espacios, academicos, no_academicos = generator.generate_espacios(n=num_spaces)
    schema.insert(espacios, "Espacio")
    espacios_academicos = generator.generate_espacio_academico(academicos, unidades)
    schema.insert(espacios_academicos, "Espacio_Academico")
    espacios_no_academicos = generator.generate_espacio_no_academico(no_academicos)
    schema.insert(espacios_no_academicos, "Espacio_No_Academico")
    print("University structure inserted successfully.")

def _link_complaints(n_people: int):
    """
    Task 3: Wipes and inserts the 'denuncias'.
    """
    schema = Schema()
    # === IDEMPOTENCY FIX: Truncate table first ===
    print("Truncating complaint links table...")
    schema.truncate_table("Denuncia")

    print("Generating complaint links (denuncias).")
    generator = DataGenerator()
    personas = generator.generate_personas(n=n_people)
    solicitantes = generator.generate_solicitantes(personas)
    denunciados = generator.generate_denunciados(personas)
    denuncias = generator.generate_denuncias(solicitantes, denunciados)
    schema.insert(denuncias, "Denuncia")
    print("Complaint links inserted successfully.")

def _create_events(n_spaces: int, n_units: int):
    """
    Task 4: Wipes and inserts the 'sucesos' (events/incidents).
    """
    schema = Schema()
    # === IDEMPOTENCY FIX: Truncate table first ===
    print("Truncating events table...")
    schema.truncate_table("Suceso")

    print("Generating events (sucesos).")
    generator = DataGenerator()

    # ### DATA GENERATION FIX: THIS SECTION IS CORRECTED ###
    # We must call generate_unidades first to align the random generator's state.
    generator.generate_unidades(n=n_units)

    # Now, this will generate the exact same list of spaces as the structure task.
    espacios, _, _ = generator.generate_espacios(n=n_spaces)

    sucesos = generator.generate_sucesos(espacios)
    schema.insert(sucesos, "Suceso")
    print("Events inserted successfully.")


# =============================================================================
# DEFINE THE AIRFLOW DAG
# =============================================================================

with DAG(
    dag_id="fill_data_v2",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@daily",
    catchup=False,
    description="DAG with 4 nodes to generate synthetic data in parallel."
) as dag:
    
    generate_people_task = PythonOperator(
        task_id="generate_people",
        python_callable=_generate_people,
        op_kwargs={"n": PEOPLE_TO_GENERATE},
    )

    generate_structure_task = PythonOperator(
        task_id="generate_university_structure",
        python_callable=_generate_university_structure,
        op_kwargs={"num_units": UNITS_TO_GENERATE, "num_spaces": SPACES_TO_GENERATE},
    )

    link_complaints_task = PythonOperator(
        task_id="link_complaints",
        python_callable=_link_complaints,
        op_kwargs={"n_people": PEOPLE_TO_GENERATE},
    )

    create_events_task = PythonOperator(
        task_id="create_events",
        python_callable=_create_events,
        # ### DATA GENERATION FIX: Pass both arguments ###
        op_kwargs={"n_spaces": SPACES_TO_GENERATE, "n_units": UNITS_TO_GENERATE},
    )

    # --- Set Task Dependencies ---
    generate_people_task >> link_complaints_task
    generate_structure_task >> create_events_task