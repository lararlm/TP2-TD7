# In file: td7/schema.py

import psycopg2
from psycopg2.extras import execute_values
from typing import List, Dict
from airflow.providers.postgres.hooks.postgres import PostgresHook

Record = Dict[str, any]
Records = List[Record]

class Schema:
    def __init__(self):
        hook = PostgresHook(postgres_conn_id="postgres_default")
        self.connection = hook.get_conn()
        self.connection.autocommit = True

    # --- THIS IS THE MISSING FUNCTION THAT NEEDS TO BE ADDED ---
    def truncate_table(self, table: str):
        """Truncates a table using CASCADE to handle foreign keys."""
        with self.connection.cursor() as cur:
            try:
                # Using CASCADE will automatically truncate dependent tables.
                # RESTART IDENTITY resets auto-incrementing counters.
                query = f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;'
                cur.execute(query)
                print(f"[OK] Truncated table {table}")
            except Exception as e:
                print(f"[ERROR] Failed to truncate {table}: {e}")
                raise

    def insert(self, records: Records, table: str):
        if not records:
            print(f"[INFO] No records to insert into {table}")
            return
        
        # Best practice: quote identifiers to handle case-sensitivity
        columns = records[0].keys()
        values = [[r.get(col) for col in columns] for r in records]
        col_str = ", ".join(f'"{c}"' for c in columns)
        
        with self.connection.cursor() as cur:
            # Quote the table name as well
            query = f'INSERT INTO "{table}" ({col_str}) VALUES %s'
            try:
                execute_values(cur, query, values)
                print(f"[OK] Inserted {len(values)} rows into {table}")
            except Exception as e:
                print(f"[ERROR] Failed to insert into {table}: {e}")
                raise