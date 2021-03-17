### Procedure

- docker-compose up -d

Make sure all services are up and running.
NOTE: phpweb is often down at first because postgres is still starting. Wait a few seconds,
re-run docker-compose up -d and phpweb will come online.

NOTE: To rebuild the entire docker container:
docker-compose up --build --force-recreate --no-deps -d

- now go to Flower UI:  http://127.0.0.1:5010

You should see a few failed tasks (which we haven't scheduled yet)

- now go to phpmyadmin UI: http://127.0.0.1:8080
  - server: mysqldb:3306
  - user: admin
  - pwd: password

You should see all available sma data from our cloud db in the tables.

- now go to Grafana: http://127.0.0.1:7000  (credentials: admin/password)

Click on "add data source"

Name: mysql

- Type: mysql

- Host: mysql

- Database: same as digitalocean db 

- User: same as digitalocean db username

- Password: same as digitalocean db password

- SSL mode: disable

Then click on "create a dashboard", type "Graph". When your graph panel is created,

Click on its title and then on "Edit".

Select mysql data source, and for the query, enter your query. 

Click on the "eye" icon on the right to test the query. You should see a graph.

Then click on "Save dashboard" on the top menu.



## Login to TWS Live
- You should now be able to login to TWS Live using VNC Viewer:

  - Remote Host Connection:   http://127.0.0.1:5904
  - Password:   root

In this way, you can run and trade in TWS Live as you normally would, while the paper trading algorithm can continue running with shared market data 
subscription.


### Functional Notes

The logic is implemented in the celery python worker, in worker/tasks.py and script.py

In order to update the logic, go and read ib_insync package documentation (https://github.com/erdewit/ib_insync). You'll probably want first to fetch more diverse data, and then, ultimately,
to code a trading strategy and place buy/sell orders. To achieve this, you'll need to understand the ib_insync calls and use them in the python worker logic.

Of course, you might have to create new tables in the Postgres DB, if you start fetching new kinds of data.

You can edit the app.conf.beat_schedule dict in worker/tasks.py to edit the frequency at which
Celery Beat runs the tasks you created.


### NOTES

- we used https://github.com/ryankennedyio/ib-docker (with some fixes) for tws docker (ib-docker folder)
- we made a specific celery dockerfile in python 3 with the right libs, in celery-ib folder
