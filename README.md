


### Procedure

- create an account on Interactive Broker website, to get an id and a password

- git clone from this repository and cd into it

- in docker-compose.yml, edit the TWSUSERID and TWSPASSWORD environment variables

- docker-compose up -d

Make sure all services are up and running.
NOTE: pgweb is often down at first because postgres is still starting. Wait a few seconds,
re-run docker-compose up -d and pgweb will come online.

- create the table in the database

docker-compose exec postgres /bin/bash
psql --username=trading
\i /init/init.sql;
\q
exit

- now go to Flower UI:  http://127.0.0.1:5010

You should see a few failed tasks (when we hadn't created yet the DB table), and the latest
tasks must be successful.

- now go to pgweb UI: http://127.0.0.1:8080

You should see some records in the forex_data_eurusd table.

- now go to Grafana: http://127.0.0.1:7000  (credentials: admin/password)

Click on "add data source"

Name: postgres

Type: PostgreSQL

Host: postgres

Database: trading (see .env file)

User: trading (see .env file)

Password: trading (see .env file)

SSL mode: disable

Then click on "create a dashboard", type "Graph". When your graph panel is created,

Click on its title and then on "Edit".

Select Postgres data source, and for the query, enter:

SELECT
  $__time(time),
  value_open
FROM
  forex_data_eurusd
WHERE
  $__timeFilter(time)

Click on the "eye" icon on the right to test the query. You should see a graph.

Then click on "Save dashboard" on the top menu.


That's it! You now have a fully functioning automated trading platform!



### Functional Notes

The logic is implemented in the celery python worker, in worker/tasks.py and script.py

In order to update the logic, go and read ib_insync package documentation (https://github.com/erdewit/ib_insync). You'll probably want first to fetch more diverse data, and then, ultimately,
to code a trading strategy and place buy/sell orders. To achieve this, you'll need to understand the ib_insync calls and use them in the python worker logic.

Of course, you might have to create new tables in the Postgres DB, if you start fetching new kinds of data.

You can edit the app.conf.beat_schedule dict in worker/tasks.py to edit the frequency at which
Celery Beat runs the tasks you created.



### NOTES

- we used https://github.com/ryankennedyio/ib-docker (with some fixes) for tws docker (ib-docker folder)

- we downloaded IB api python client (source/pythonclient/ibapi) (here, "ibapi" folder) and make it available to python workers through a docker volume mapping.

- we made a specific celery dockerfile in python 3 with the right libs, in celery-ib folder
