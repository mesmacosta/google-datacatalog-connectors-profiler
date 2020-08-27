import argparse
import random
import uuid
import time

from teradatasql import connect

_DATA_TYPES = [
    'INTEGER', 'CHAR(25)', 'DECIMAL(8,2)', 'DATE', 'VARCHAR(25)', 'SMALLINT',
    'CHAR', 'BYTEINT'
]

_COLUMN_NAMES = [
    'name', 'address', 'city', 'state', 'date_time', 'paragraph', 'randomdata',
    'person', 'credit_card', 'size', 'reason', 'school', 'food', 'location',
    'house', 'price', 'cpf', 'cnpj', 'passport', 'security_number',
    'phone_number', 'bank_account_number', 'ip_address', 'stocks'
]

_TABLE_NAMES = [
    'school_info', 'personal_info', 'persons', 'employees', 'companies',
    'store', 'home'
]

_DATABASE_NAMES = [
    'school_warehouse', 'company_warehouse', 'on_prem_warehouse',
    'factory_warehouse', 'organization_warehouse'
]


def get_conn(connection_args):
    return connect(None,
                   host=connection_args['host'],
                   user=connection_args['user'],
                   password=connection_args['pass'])


def create_random_metadata(connection_args):
    conn = None
    cursor = None

    try:
        conn = get_conn(connection_args)
        cursor = conn.cursor()
    except:
        conn, cursor = create_cursor_loop(connection_args, 15)

    for x in range(connection_args['number_databases']):
        database_name, database_stmt = build_create_database_statement()
        cursor.execute(database_stmt)
        for y in range(connection_args['number_tables']):
            query = build_create_table_statement(database_name)
            print('\n' + query)
            cursor.execute(query)
        conn.commit()

    cursor.close()
    conn.close()


def create_cursor_loop(connection_args, times):
    print('Teradata Server not ready. Trying again')
    for i in range(times):
        try:
            time.sleep(10 + 10 * i)
            conn = get_conn(connection_args)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as err:
            print('Attempt: {}, Teradata Server not ready.'.format(i))


def get_random_database_name():
    return random.choice(_DATABASE_NAMES)


def build_create_database_statement():
    database_name = '{}{}'.format(get_random_database_name(),
                                  str(random.randint(1, 100000)))
    database_stmt = 'CREATE DATABASE "{}" AS '.format(database_name)
    database_stmt += 'PERM = 2000000*(HASHAMP()+1), '
    database_stmt += 'SPOOL = 2000000*(HASHAMP()+1), '
    database_stmt += 'TEMPORARY = 2000000*(HASHAMP()+1) '
    return database_name, database_stmt


def get_random_data_type():
    return random.choice(_DATA_TYPES)


def get_random_column_name():
    return random.choice(_COLUMN_NAMES)


def get_random_table_name():
    return random.choice(_TABLE_NAMES)


def build_create_table_statement(database_name):
    table_stmt = 'CREATE TABLE {}.{}{} ( '.format(database_name,
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
        description='Command line generate random metadata into teradata')
    parser.add_argument('--teradata-host',
                        help='Your teradata server host, this is required even'
                        ' for the raw_metadata_csv,'
                        ' so we are able to map the created entries'
                        ' resource with the teradata host',
                        required=True)
    parser.add_argument('--teradata-user',
                        help='Your teradata credentials user')
    parser.add_argument('--teradata-pass',
                        help='Your teradata credentials password')
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

    create_random_metadata({
        'host': args.teradata_host,
        'user': args.teradata_user,
        'pass': args.teradata_pass,
        'number_databases': args.number_databases,
        'number_tables': args.number_tables
    })
