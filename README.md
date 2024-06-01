# Template para TP 


## Estado

- [x] Generación de datos con Faker
- [x] Airflow
- [] Proyecto DBT
- [] DAG de generación de datos
- [] DAG de transformación de datos con DBT


## Instrucciones para correr sin Docker

```
airflow db migrate && airflow users create --username airflow --firstname Peter --lastname Parker --role Admin --password airflow --email spiderman@superhero.org
airflow webserver --port 8080 & airflow scheduler &
```

## Instrucciones para correr con Docker


