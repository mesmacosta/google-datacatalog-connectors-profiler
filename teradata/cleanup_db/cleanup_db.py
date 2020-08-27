import argparse
import sys
import uuid

from teradatasql import connect

QUERY = """
SELECT DISTINCT
      d.DatabaseName as database_name
  FROM DBC.DatabasesV d
  WHERE d.DatabaseName NOT IN ('All',
          'console',
          'viewpoint',
          'Crashdumps',
          'DBC', 'dbcmngr',
          'Default', 'External_AP', 'EXTUSER',
          'LockLogShredder', 'PUBLIC', 'SQLJ',
          'Sys_Calendar', 'SysAdmin', 'SYSBAR',
          'SYSJDBC', 'SYSLIB', 'SYSSPATIAL',
          'SystemFe', 'SYSUDTLIB', 'SYSUIF',
          'TD_SERVER_DB', 'TD_SYSFNLIB',
          'TD_SYSGPL', 'TD_SYSXML', 'TDMaps',
          'TDPUSER', 'TDQCD', 'TDStats', 'tdwm')
  ORDER BY d.DatabaseName;
"""


def get_conn(connection_args):
    return connect(None,
                   host=connection_args['host'],
                   user=connection_args['user'],
                   password=connection_args['pass'])


def cleanup_metadata(connection_args):
    conn = get_conn(connection_args)

    cursor = conn.cursor()
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    for row in rows:
        try:
            database_name = row[0]
            delete_database_stmt, drop_database_stmt = build_drop_database_statement(
                database_name)
            cursor.execute(delete_database_stmt)
            cursor.execute(drop_database_stmt)
            print('Cleaned database: {}'.format(database_name))
            conn.commit()
        except:
            print('Database: {} not deleted.'.format(database_name))

    cursor.close()


def build_drop_database_statement(database_name):
    delete_database_stmt = 'DELETE DATABASE {}'.format(database_name)
    drop_database_stmt = 'DROP DATABASE {}'.format(database_name)
    return delete_database_stmt, drop_database_stmt


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command line to cleanup metadata from teradata')
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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    cleanup_metadata({
        'host': args.teradata_host,
        'user': args.teradata_user,
        'pass': args.teradata_pass
    })
