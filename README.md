# Template para TP


## Estado

- [x] Generación de datos con Faker
- [x] Airflow
- [x] Proyecto DBT
- [ ] DAG de generación de datos
- [x] DAG de transformación de datos con DBT
- [ ] Chequear si es más liviana la imagen con pip sobre poetry


## Instrucciones para correr sin Docker

```
airflow db migrate && airflow users create --username airflow --firstname Peter --lastname Parker --role Admin --password airflow --email spiderman@superhero.org
airflow webserver --port 8080 & airflow scheduler &
```

## Instrucciones para correr con Docker


## Pasos para desarrollar el TP

1. Poner los statements para crear las tablas en sql/create_tables.sql.
2. Modificar las funciones de obtención de datos en td7/schema.py.
3. Escribir los generadores de datos en td7/data_generator.py.
4. Armar el o los DAGs necesarios en dags/.
    1. Un ejemplo de un nodo para cargar datos está en dags/fill_data.py.
    2. Un ejemplo de un nodo para correr transformaciones está en dags/run_dbt.py.


Si quieren agregar dependencias pueden usar:

```
poetry add <dependencia>
poetry export --without-hashes --format=requirements.txt > requirements.txt
docker compose build
```

o directamente modificar el requirements.txt y correr el build de nuvo.

## Pasos para correr DBT a mano
```bash
docker compose run dbt <COMMAND>
```

## Ver documentación de DBT
En la UI de Airflow -> `Browse` --> `dbt Docs`
