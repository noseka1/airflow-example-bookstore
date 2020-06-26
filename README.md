# airflow-example-bookstore
Example Airflow DAG

Drop the `bookstore.py` DAG into your $AIRFLOW_HOME/dags directory. Verify that the DAG was successully added to Airflow:

```
$ airflow list_dags | grep bookstore
bookstore
```

Set the schedule date:

```
$ DATE=$(date --iso-8601=date)
```

Create input data:

```
$ mkdir /tmp/bookstore
$ echo '{"rate": 1.2 }' > /tmp/bookstore/rate-$DATE.json
$ echo '{"revenue": 20 }' > /tmp/bookstore/revenue-$DATE.json
```

Clear previous runs:

```
$ airflow clear --no_confirm -s $DATE -e $DATE bookstore
```

Start the DAG:

```
$ airflow backfill bookstore -s $DATE -e $DATE
```

Print out the result:

```
$ cat /tmp/bookstore/revenue-report-$DATE.json
```
