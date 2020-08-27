import argparse
import logging
import random
import sys
import uuid
import time

from cx_Oracle import connect

_DATA_TYPES = [
    'INTEGER', 'NUMBER(10,2)', 'VARCHAR2(10 char)', 'BLOB', 'DATE', 'TIMESTAMP'
]

_COLUMN_NAMES = [
    'name', 'address', 'city', 'state', 'date_time', 'paragraph', 'randomdata',
    'person', 'credit_card', 'size', 'reason', 'school', 'food', 'location',
    'house', 'price', 'cpf', 'cnpj', 'passport', 'security_number',
    'phone_number', 'bank_account_number', 'ip_address', 'stocks'
]

_DESCRIPTION_VALUES = [
    'This is a random generated column',
    'Description for random generated column'
]

_TABLE_NAMES = [
    'school_info', 'personal_info', 'persons', 'employees', 'companies',
    'store', 'home'
]


def get_conn(connection_args):
    return connect(connection_args['user'],
                   connection_args['pass'],
                   '{}:{}/{}'.format(connection_args['host'],
                                     connection_args['port'],
                                     connection_args['db_service']),
                   encoding='UTF-8')


def create_random_metadata(connection_args):
    conn = None
    cursor = None

    try:
        conn = get_conn(connection_args)
        cursor = conn.cursor()
    except:
        conn, cursor = create_cursor_loop(connection_args, 5)

    for x in range(connection_args['number_tables']):
        query = build_create_table_statement()
        print('\n' + query)
        cursor.execute(query)

    conn.commit()
    cursor.close()


def create_cursor_loop(connection_args, times):
    logging.info('Oracle listener not ready. Trying again')
    for i in range(times):
        try:
            time.sleep(10 + 10 * i)
            conn = get_conn(connection_args)
            cursor = conn.cursor()
            return conn, cursor
        except:
            logging.info('Attempt: {}, Oracle listener not ready.'.format(i))


def get_random_data_type():
    return random.choice(_DATA_TYPES)


def get_random_column_name():
    return random.choice(_COLUMN_NAMES)


def get_random_column_description():
    return random.choice(_DESCRIPTION_VALUES)


def get_random_table_name():
    return random.choice(_TABLE_NAMES)


# This uses the HR schema that comes with the oracle express edition,
# if you have a different schema you can change that
def build_create_table_statement(schema='hr'):
    table_stmt = 'CREATE TABLE {}.{}{} ( '.format(schema,
                                                  get_random_table_name(),
                                                  uuid.uuid4().hex[:8])
    table_stmt = '{}{}{} {}'.format(table_stmt, get_random_column_name(),
                                    str(random.randint(1, 100000)),
                                    get_random_data_type())
    for x in range(random.randint(1, 15)):
        table_stmt += ', {}{}'.format(get_random_column_name(),
                                      str(random.randint(1, 100000))) + \
            ' {}'.format(get_random_data_type())

    table_stmt = '{} )'.format(table_stmt)
    return table_stmt


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command line generate random metadata into oracle')
    parser.add_argument('--oracle-host',
                        help='Your oracle server host, this is required even'
                        ' for the raw_metadata_csv,'
                        ' so we are able to map the created entries'
                        ' resource with the mysql host',
                        required=True)
    parser.add_argument('--oracle-user', help='Your oracle credentials user')
    parser.add_argument('--oracle-port', help='Your Oracle server port')
    parser.add_argument('--oracle-pass',
                        help='Your oracle credentials password')
    parser.add_argument('--oracle-db-service',
                        help='Your Oracle database service name')
    parser.add_argument('--number-tables',
                        help='Number of tables to create',
                        type=int,
                        default=1000)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Enable logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    create_random_metadata({
        'db_service': args.oracle_db_service,
        'host': args.oracle_host,
        'port': args.oracle_port,
        'user': args.oracle_user,
        'pass': args.oracle_pass,
        'number_tables': args.number_tables
    })
