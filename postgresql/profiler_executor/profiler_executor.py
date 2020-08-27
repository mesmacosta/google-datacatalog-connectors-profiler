import sys
import datetime
import logging

from google.datacatalog_connectors.postgresql import datacatalog_cli
from ciandt.google_cloud import metrics_collector

if __name__ == "__main__":
    sys.argv.extend(['--enable-monitoring', 'true'])

    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    now = datetime.datetime.now()

    start_time = now.strftime('%m/%d/%y %H:%M:%S')

    datacatalog_cli.PostgreSQL2DatacatalogCli().run()

    now = datetime.datetime.now()

    end_time = now.strftime('%m/%d/%y %H:%M:%S')

    sys.argv.extend(['--entry-group-id', 'postgresql'])
    sys.argv.extend(['--start-time', start_time])
    sys.argv.extend(['--end-time', end_time])
    sys.argv.extend(['--generate-csv', 'true'])

    metrics_collector.MetricsCollectorCli.run()
