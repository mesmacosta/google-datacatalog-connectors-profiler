import sys
import datetime
import logging

from google.datacatalog_connectors.apache_atlas import apache_atlas2datacatalog_cli
from ciandt.google_cloud import metrics_collector

if __name__ == "__main__":
    sys.argv.extend(['--enable-monitoring', 'true'])

    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    now = datetime.datetime.now()

    start_time = now.strftime('%m/%d/%y %H:%M:%S')

    apache_atlas2datacatalog_cli.main()

    now = datetime.datetime.now()

    end_time = now.strftime('%m/%d/%y %H:%M:%S')

    sys.argv.extend(['--entry-group-id', 'apache_atlas'])
    sys.argv.extend(['--datacatalog-location-id', 'us-central1'])
    sys.argv.extend(['--start-time', start_time])
    sys.argv.extend(['--end-time', end_time])
    sys.argv.extend(['--generate-csv', 'true'])

    metrics_collector.MetricsCollectorCli.run()
