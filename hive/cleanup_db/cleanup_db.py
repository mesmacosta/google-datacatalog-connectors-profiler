import argparse
import sys
import uuid

from pyhive.hive import connect

QUERY = 'show databases'


def get_conn(connection_args):
    return connect(host=connection_args['host'],
                   port=connection_args['port'],
                   username=connection_args['user'],
                   database=connection_args['database'],
                   auth=None)


def cleanup_metadata(connection_args):
    conn = get_conn(connection_args)

    cursor = conn.cursor()
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    for row in rows:
        database_name = row[0]
        database_stmt = build_drop_database_cascade_statement(database_name)
        if database_name != 'default':
            cursor.execute(database_stmt)
            print('Cleaned database: {}'.format(database_name))
            conn.commit()

    cursor.close()


def build_drop_database_cascade_statement(database_name):
    database_stmt = 'DROP DATABASE {} CASCADE'.format(database_name)
    return database_stmt


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command line to cleanup metadata from hive')
    parser.add_argument('--hive-host',
                        help='Your Hive server host',
                        required=True)
    parser.add_argument('--hive-user', help='Your Hive server user')
    parser.add_argument('--hive-database',
                        help='Your Hive server database name')
    parser.add_argument('--hive-port',
                        help='Your Hive server port',
                        type=int,
                        default=1000)
    parser.add_argument('--number-databases',
                        help='Number of databases to create',
                        type=int,
                        default=4)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    cleanup_metadata({
        'database': args.hive_database,
        'host': args.hive_host,
        'user': args.hive_user,
        'port': args.hive_port
    })
