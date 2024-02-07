import psycopg

from common_packages import jinja_helper
from pathlib import Path

_sql_query_path = Path('./resources/sql')


def bulk_copy_file(connection_url, filepath, table, columns, file_format, delimiter=None, header_option=None):
    data = {
        'table': table,
        'columns': columns,
        'file_format': file_format,
    }
    if delimiter is not None:
        data['delimiter'] = delimiter
    if header_option is not None:
        data['header_option'] = header_option
    copy_cmd = jinja_helper.render_jinja2_template(_sql_query_path, 'copy_cmd.j2', data)
    print(copy_cmd)
    with open(filepath, 'r') as f:
        with psycopg.connect(connection_url) as conn:
            with conn.cursor() as cursor:
                with cursor.copy(copy_cmd) as copy:
                    copy.write(f.read())
