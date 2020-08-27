import argparse
import logging
import sys
import uuid

from cx_Oracle import connect

QUERY = """
SELECT
     DISTINCT tab.owner as schema_name,
     tab.table_name as table_name
FROM all_tables tab
WHERE tab.owner in
  (select username from all_users
   where oracle_maintained = 'N')
"""


def get_conn(connection_args):
    return connect(connection_args['user'],
                   connection_args['pass'],
                   '{}:{}/{}'.format(connection_args['host'],
                                     connection_args['port'],
                                     connection_args['db_service']),
                   encoding='UTF-8')


def cleanup_metadata(connection_args):
    conn = get_conn(connection_args)

    cursor = conn.cursor()
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    for row in rows:
        schema_name = row[0]
        table_name = row[1]
        table_stmt = build_drop_table_statement(schema_name, table_name)
        cursor.execute(table_stmt)
        print('Cleaned table: {}.{}'.format(schema_name, table_name))
        conn.commit()

    cursor.close()


def build_drop_table_statement(schema_name, table_name):
    table_stmt = 'DROP TABLE {}.{} CASCADE CONSTRAINTS'.format(
        schema_name, table_name)
    return table_stmt


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command line to cleanup metadata from oracle')
    parser.add_argument('--oracle-host',
                        help='Your oracle server host, this is required even'
                        ' for the raw_metadata_csv,'
                        ' so we are able to map the created entries'
                        ' resource with the oracle host',
                        required=True)
    parser.add_argument('--oracle-user', help='Your oracle credentials user')
    parser.add_argument('--oracle-port', help='Your Oracle server port')
    parser.add_argument('--oracle-pass',
                        help='Your oracle credentials password')
    parser.add_argument('--oracle-db-service',
                        help='Your Oracle database service name')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    cleanup_metadata({
        'db_service': args.oracle_db_service,
        'host': args.oracle_host,
        'port': args.oracle_port,
        'user': args.oracle_user,
        'pass': args.oracle_pass
    })
