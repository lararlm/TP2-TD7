from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator

EVENTS_PER_DAY = 10_000


def generate_data(base_time: str, n: int):
    """Generates synth data and saves to DB.

    Parameters
    ----------
    base_time: str
        Base datetime to start events from.
    n : int
        Number of events to generate.
    """
    generator = DataGenerator()
    people = generator.generate_people()

    sessions = generator.generate_sessions(
        people,
        datetime.datetime.fromisoformat(base_time),
        datetime.timedelta(days=1),
        n,
    )
    # TODO: save to DB


with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    op = PythonOperator(
        task_id="task",
        python_callable=generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
    )
