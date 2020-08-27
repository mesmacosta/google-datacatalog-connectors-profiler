import argparse
import sys
import datetime
import logging

from google.datacatalog_connectors.teradata import datacatalog_cli
from ciandt.google_cloud import metrics_collector


def __parse_args():
    parser = argparse.ArgumentParser(
        description='Command line generate random metadata into mysql')
    parser.add_argument('--teradata-host',
                        help='Your Teradata server host,'
                        ' this is required even'
                        ' for the raw_metadata_csv,'
                        ' so we are able to map the created entries'
                        ' resource with the teradata host',
                        required=True)
    parser.add_argument('--teradata-user',
                        help='Your Teradata credentials user')
    parser.add_argument('--teradata-pass',
                        help='Your Teradata credentials password')
    args, unknown = parser.parse_known_args()
    return args


def __force_teradata_connection():
    args = __parse_args()
    import teradatasql
    teradatasql.connect(None,
                        host=args.teradata_host,
                        user=args.teradata_user,
                        password=args.teradata_pass)


if __name__ == "__main__":
    # The teradatasql library uses a dll to connect to the teradata database
    # the loading process must occur in the main thread, so we connect to it
    # here to force the load.
    __force_teradata_connection()

    sys.argv.extend(['--enable-monitoring', 'true'])

    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    now = datetime.datetime.now()

    start_time = now.strftime('%m/%d/%y %H:%M:%S')

    datacatalog_cli.Teradata2DatacatalogCli().run()

    now = datetime.datetime.now()

    end_time = now.strftime('%m/%d/%y %H:%M:%S')

    sys.argv.extend(['--entry-group-id', 'teradata'])
    sys.argv.extend(['--start-time', start_time])
    sys.argv.extend(['--end-time', end_time])
    sys.argv.extend(['--generate-csv', 'true'])

    metrics_collector.MetricsCollectorCli.run()
