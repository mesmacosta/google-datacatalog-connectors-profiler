import argparse
import random
import uuid
import time

from pyhive import hive

_DATA_TYPES = [
    'TINYINT', 'SMALLINT', 'INT', 'BIGINT', 'FLOAT', 'DOUBLE', 'DECIMAL',
    'TIMESTAMP', 'DATE', 'STRING', 'BOOLEAN', 'BINARY',
    'ARRAY<STRUCT< key:STRING, value:STRING>>', 'ARRAY <STRING>',
    'ARRAY <STRUCT <spouse: STRING, children: ARRAY <STRING>>>',
    'ARRAY<DOUBLE>', 'MAP<STRING,DOUBLE>',
    'STRUCT < employer: STRING, id: BIGINT, address: STRING >',
    'UNIONTYPE<DOUBLE, STRING, ARRAY<string>, STRUCT<a:INT,b:string>>'
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

_DATABASE_NAMES = [
    'school_warehouse', 'company_warehouse', 'on_prem_warehouse',
    'factory_warehouse', 'organization_warehouse'
]


def get_hive_conn(connection_args):
    return hive.connect(host=connection_args['host'],
                        port=connection_args['port'],
                        username=connection_args['user'],
                        database=connection_args['database'],
                        auth=None)


def create_random_hive_data(connection_args):
    conn = None
    cursor = None

    try:
        conn = get_hive_conn(connection_args)
        cursor = conn.cursor()
    except:
        conn, cursor = create_cursor_loop(connection_args, 5)

    for x in range(connection_args['number_databases']):
        database_name, database_stmt = build_create_database_statement()
        print('\n' + database_stmt)
        cursor.execute(database_stmt)
        cursor.execute(build_use_database_statement(database_name))
        for y in range(connection_args['number_tables']):
            table_name, table_stmt = build_create_table_statement()
            cursor.execute(table_stmt)
            print('\n Created table:' + table_name)

    cursor.execute('show databases')
    databases = cursor.fetchall()
    print(databases)

    cursor.close()
    conn.close()


def create_cursor_loop(connection_args, times):
    print('Hive Server not ready. Trying again')
    for i in range(times):
        try:
            time.sleep(10 + 10 * i)
            conn = get_hive_conn(connection_args)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as err:
            print('Attempt: {}, Hive Server not ready.'.format(i))


def get_random_data_type():
    return random.choice(_DATA_TYPES)


def get_random_databases_name():
    return random.choice(_DATABASE_NAMES)


def get_random_column_name():
    return random.choice(_COLUMN_NAMES)


def get_random_column_description():
    return random.choice(_DESCRIPTION_VALUES)


def get_random_table_name():
    return random.choice(_TABLE_NAMES)


def build_create_database_statement():
    database_name = '{}{}'.format(get_random_databases_name(),
                                  uuid.uuid4().hex[:8])
    database_stmt = 'CREATE DATABASE {} '.format(database_name)
    return database_name, database_stmt


def build_use_database_statement(database_name):
    return 'USE {} '.format(database_name)


def build_create_table_statement():
    table_name = '{}{}'.format(get_random_table_name(), uuid.uuid4().hex[:8])
    table_stmt = 'CREATE TABLE {} ( '.format(table_name)
    table_stmt = '{}{}{} {}'.format(table_stmt, get_random_column_name(),
                                    uuid.uuid4().hex[:8],
                                    get_random_data_type())
    for x in range(random.randint(1, 100)):
        table_stmt += ' , {}{}'.format(get_random_column_name(), uuid.uuid4().hex[:8]) + \
            '  {}'.format(get_random_data_type()) + \
            ' COMMENT "{}"'.format(get_random_column_description())

    table_stmt = '{} )'.format(table_stmt)
    return table_name, table_stmt


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command line generate random metadata into a Hive server')
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
    parser.add_argument('--number-tables',
                        help='Number of tables to create',
                        type=int,
                        default=250)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    create_random_hive_data({
        'database': args.hive_database,
        'host': args.hive_host,
        'user': args.hive_user,
        'port': args.hive_port,
        'number_databases': args.number_databases,
        'number_tables': args.number_tables
    })
