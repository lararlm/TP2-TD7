# Template para TP 



## Instrucciones para correr sin Docker

```
airflow db migrate && airflow users create --username airflow --firstname Peter --lastname Parker --role Admin --password airflow --email spiderman@superhero.org
airflow webserver --port 8080 & airflow scheduler &
```