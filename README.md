# airflow-example-bookstore
Example Airflow DAG

Set the schedule date:

```
$ DATE=$(date --iso-8601=date)
```

Create input data:

```
$ echo '{"rate": 1.2 }' > /tmp/bookstore-rate-$DATE.json
$ echo '{"revenue": 20 }' > /tmp/bookstore-revenue-$DATE.json
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
$ bookstore-revenue-converted-$DATE.json
```
