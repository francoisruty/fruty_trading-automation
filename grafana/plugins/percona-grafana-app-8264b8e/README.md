### About

This app provides a set of dashboards for MySQL performance and system monitoring with Prometheus datasource.
The dashboards rely on `alias` label in the Prometheus config and depend from the small patch applied on Grafana.

### Dashboards

 * Cross Server Graphs
 * Disk Performance
 * Disk Space
 * Galera Graphs
 * MySQL InnoDB Metrics
 * MySQL MyISAM Metrics
 * MySQL Overview
 * MySQL Performance Schema
 * MySQL Query Response Time
 * MySQL Replication
 * MySQL Table Statistics
 * MySQL User Statistics
 * Prometheus
 * Summary Dashboard
 * System Overview
 * TokuDB Graphs
 * Trends Dashboard

### Screenshots

![img](https://raw.githubusercontent.com/percona/grafana-dashboards/master/assets/sample2.png)
![img](https://raw.githubusercontent.com/percona/grafana-dashboards/master/assets/sample5.png)
![img](https://raw.githubusercontent.com/percona/grafana-dashboards/master/assets/sample6.png)

### Setup instructions

#### Import dashboards

Enable the plugin and import the necessary dashboards from plugin's Dashboards tab.

#### Add Prometheus datasource

The datasource should be named `Prometheus` so it is automatically picked up by the graphs.

#### Prometheus configuration

The dashboards use `alias` label to work with individual hosts.
Ensure you have `alias` defined for each of your targets.
For example, if you want to monitor `192.168.1.7` the excerpt of the config will be look like this:

    scrape_configs:
      - job_name: prometheus
        target_groups:
          - targets: ['localhost:9090']

      - job_name: linux
        target_groups:
          - targets: ['192.168.1.7:9100']
            labels:
              alias: db1

      - job_name: mysql
        target_groups:
          - targets: ['192.168.1.7:9104']
            labels:
              alias: db1

Note, adding a new label to the existing Prometheus instance will introduce a mess with the time-series.
So it is recommended to start using `alias` from scratch.

How you name jobs is not important. However, "Prometheus" dashboard assumes the job name is `prometheus`.

Also it is assumed that the exporters are run at least with this minimal set of options:

 * node_exporter: `-collectors.enabled="diskstats,filesystem,loadavg,meminfo,netdev,stat,time,uname,vmstat"`
 * mysqld_exporter: `-collect.binlog_size=true -collect.info_schema.processlist=true`

##### Apply Grafana patch

It is important to apply the following minor patch on your Grafana installation in order to use the interval template variable to get the good zoomable graphs. The fix is simply to allow variable in Step field of graph editor page. For more information, take a look at [PR#3757](https://github.com/grafana/grafana/pull/3757) and [PR#4257](https://github.com/grafana/grafana/pull/4257).

Run those 2 commands on top of your Grafana installation:

    sed -i 's/expr=\(.\)\.replace(\(.\)\.expr,\(.\)\.scopedVars\(.*\)var \(.\)=\(.\)\.interval/expr=\1.replace(\2.expr,\3.scopedVars\4var \5=\1.replace(\6.interval, \3.scopedVars)/' /usr/share/grafana/public/app/plugins/datasource/prometheus/datasource.js

    sed -i 's/,range_input/.replace(\/"{\/g,"\\"").replace(\/}"\/g,"\\""),range_input/; s/step_input:""/step_input:this.target.step/' /usr/share/grafana/public/app/plugins/datasource/prometheus/query_ctrl.js

Those changes are idemportent and do not break anything. No restart required.

#### Changelog

##### v1.0.0
- Initial version.
