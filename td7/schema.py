from psycopg2.extras import execute_values
from typing import List, Dict
from airflow.providers.postgres.hooks.postgres import PostgresHook

Record = Dict[str, any]
Records = List[Record]

class Schema:
    def __init__(self):
        hook = PostgresHook(postgres_conn_id="postgres")
        self.connection = hook.get_conn()
        self.connection.autocommit = True

    def truncate_table(self, table: str):
        """Truncates a table using CASCADE to handle foreign keys."""
        with self.connection.cursor() as cur:
            try:
                query = f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;'
                cur.execute(query)
                print(f"[OK] Truncated table {table}")
            except Exception as e:
                print(f"[ERROR] Failed to truncate {table}: {e}")
                raise

    def insert(self, records: Records, table: str):
        if not records:
            print(f"[INFO] No records to insert into {table}")
            return
        
        columns = records[0].keys()
        values = [[r.get(col) for col in columns] for r in records]
        col_str = ", ".join(columns) 
        
        with self.connection.cursor() as cur:
            query = f'INSERT INTO {table} ({col_str}) VALUES %s'
            try:
                execute_values(cur, query, values)
                print(f"[OK] Inserted {len(values)} rows into {table}")
            except Exception as e:
                print(f"[ERROR] Failed to insert into {table}: {e}")
                raise