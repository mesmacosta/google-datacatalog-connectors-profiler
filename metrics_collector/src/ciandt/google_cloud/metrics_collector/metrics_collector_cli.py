import argparse
import logging
import sys
from datetime import datetime

import pandas as pd

from google.datacatalog_connectors.commons import monitoring


class MetricsCollectorCli:

    @staticmethod
    def run():
        args, unknown = MetricsCollectorCli.__parse_args()
        # Enable logging
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        MetricsCollectorCli.___collect_metrics({
            'project_id': args.datacatalog_project_id,
            'location_id': args.datacatalog_location_id,
            'entry_group_id': args.entry_group_id,
            'start_time': args.start_time,
            'end_time': args.end_time,
            'generate_csv': args.generate_csv
        })

    @staticmethod
    def __parse_args():
        parser = argparse.ArgumentParser(
            description='Command line generate random metadata into mysql')
        parser.add_argument('--datacatalog-project-id',
                            help='Project ID where your metrics are stored',
                            required=True)
        parser.add_argument('--datacatalog-location-id',
                            help='Location ID where your metrics are stored',
                            required=True)
        parser.add_argument('--entry-group-id',
                            help='Entry group ID of your metrics')
        parser.add_argument('--start-time',
                            help='Start time of collection, '
                            'format: dd/mm/yy hh:mm:ss')
        parser.add_argument('--end-time',
                            help='End time of collection, '
                            'format: dd/mm/yy hh:mm:ss')
        parser.add_argument('--generate-csv',
                            help='Flag to enable CSV creation')
        return parser.parse_known_args()

    @staticmethod
    def __create_csv_from_stats(stats):
        entry_group_id = stats['entry_group_id']

        elapsed_time_metrics_row = [
            entry_group_id, 'elapsed_time_metrics',
            stats['elapsed_time_metrics']
        ]

        entries_length_metrics_row = [
            entry_group_id, 'entries_length_metrics',
            stats['entries_length_metrics']
        ]

        metadata_payload_bytes_metrics_row = [
            entry_group_id, 'metadata_payload_bytes_metrics',
            stats['metadata_payload_bytes_metrics']
        ]

        datacatalog_api_calls_row = [
            entry_group_id, 'datacatalog_api_calls',
            sum(stats['api_calls'].values())
        ]

        rows = [
            elapsed_time_metrics_row, entries_length_metrics_row,
            metadata_payload_bytes_metrics_row, datacatalog_api_calls_row
        ]

        for key, value in stats['api_calls'].items():
            rows.append([entry_group_id, key, value])

        df = pd.DataFrame(rows)
        df.columns = ['ENTRY_GROUP', 'METRIC', 'VALUE']
        df = df.set_index('ENTRY_GROUP')

        df.to_csv('metrics.csv', sep=',', encoding='utf-8')

    @staticmethod
    def ___collect_metrics(metrics_args):
        start_datetime = datetime.strptime(metrics_args['start_time'],
                                           '%m/%d/%y %H:%M:%S')

        end_datetime = datetime.strptime(metrics_args['end_time'],
                                         '%m/%d/%y %H:%M:%S')

        metrics_facade = monitoring \
            .MonitoringFacade(
                metrics_args['project_id'],
                metrics_args['location_id'],
                metrics_args['entry_group_id'])

        elapsed_time_metrics = metrics_facade.list_metrics(
            monitoring.MonitoringFacade.ELAPSED_TIME, start_datetime,
            end_datetime)
        entries_length_metrics = metrics_facade.list_metrics(
            monitoring.MonitoringFacade.ENTRIES_LENGTH, start_datetime,
            end_datetime)
        metadata_payload_bytes_metrics = metrics_facade.list_metrics(
            monitoring.MonitoringFacade.METADATA_PAYLOAD_BYTES, start_datetime,
            end_datetime)

        api_metrics = metrics_facade.list_datacatalog_apis_metric(
            start_datetime, end_datetime)

        # Get the first execution found in the given range
        stats = {
            'entry_group_id':
                metrics_args['entry_group_id'],
            'elapsed_time_metrics':
                elapsed_time_metrics[0].points[0].value.double_value,
            'entries_length_metrics':
                entries_length_metrics[0].points[0].value.double_value,
            'metadata_payload_bytes_metrics':
                metadata_payload_bytes_metrics[0].points[0].value.double_value,
            'api_calls': {}
        }
        for api_metric in api_metrics:
            api_calls_stats = stats['api_calls']

            method = api_metric.resource.labels['method']
            response_code = api_metric.metric.labels['response_code']
            method_key = '{}#{}'.format(method, response_code)
            method_stats = api_calls_stats.get(method_key)
            if not method_stats:
                method_stats = 0

            for point in api_metric.points:
                value = point.value.int64_value
                method_stats += value
            api_calls_stats[method_key] = method_stats

        if metrics_args['generate_csv']:
            MetricsCollectorCli.__create_csv_from_stats(stats)

        return stats
