import pyodbc
import Quick_Python
from typing import List


class Queries:
    """
    Container of static methods for handling player queries
    """
    @staticmethod
    def select_by_key(table_info, where_value: str) -> dict:
        """
        Select database row by key
        :param table_info: table constants containing table definitions. Where table is table name, and key is table key
        :param where_value: where value
        :return: dict containing database info
        """
        query = """\
                SELECT * 
                FROM [{table}] 
                WHERE [{key}] = ?
                """.format(**table_info.to_dict())
        args = [where_value]
        cursor = Quick_Python.run_query(query, args)

        # Convert cursor into dict with column as the key
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row is not None:
            result = dict(zip(columns, row))

        return None if not result else result

    @staticmethod
    def select_by_key(table_info, where_value: str) -> dict:
        """
        Select database row by key
        :param table_info: table constants containing table definitions. Where table is table name, and key is table key
        :param where_value: where value
        :return: dict containing database info
        """
        query = """\
                SELECT * 
                FROM [{table}] 
                WHERE [{key}] = ?
                """.format(**table_info.to_dict())
        args = [where_value]
        cursor = Quick_Python.run_query(query, args)

        # Convert cursor into dict with column as the key
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row is not None:
            result = dict(zip(columns, row))

        return None if not result else result

    @staticmethod
    def select(table_info, where_column: str, where_value: str) -> List[dict]:
        """
        Select database row by key
        :param table_info: table constants containing table definitions. Where table is table name, and key is table key
        :param where_column: column to check for value
        :param where_value: where value
        :return: dict containing database info
        """
        query = """\
                SELECT * 
                FROM [{table}] 
                WHERE [{where_column}] = ?
                """.format(**table_info.to_dict(), where_column=where_column)
        args = [where_value]
        cursor = Quick_Python.run_query(query, args)

        # Convert cursor into dict with column as the key
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return [] if not results else results

    @staticmethod
    def update_by_key(table_info, data: dict, where_value: str):
        # create set clause after splitting dictionary into keys and values
        keys, values = zip(*data.items())
        set_clause = 'SET {}'.format(', '.join('[{}]=?'.format(k) for k in keys))
        # add where_value to values for query
        values.append(where_value)
        # Construct query and run it
        query = "UPDATE [{table}] {set_clause} WHERE [{key}] = ?".format(set_clause=set_clause, **table_info.to_dict)
        Quick_Python.run_query_commit(query, values)

    @staticmethod
    def insert(table_info, data: dict):
        # get column information for table attr of table_info
        column_data = Quick_Python.get_column_names_and_types(table_info.table)
        print(column_data)
        # split data into keys and values and convert values which need to be unique ids
        keys = []
        values = []
        args = []
        for k, v in data.items():
            # add key to keys list
            keys.append(k)
            arg = v
            value = '?'
            # if matching key in table info is a unique identifier
            if column_data[k] == pyodbc.SQL_GUID:
                if arg is not None:
                    args.append(arg)
                    values.append("CONVERT(uniqueidentifier,?)")
                else:
                    values.append("NEWID()")
            else:
                args.append(arg)
                values.append('?')

        # Create column and value strings
        columns_string = ','.join("[{}]".format(k) for k in keys)
        values_string = ','.join(values)
        query = "INSERT INTO [{table}] ({columns}) VALUES ({values})".format(table=table_info.table,
                                                                             columns=columns_string,
                                                                             values=values_string)
        Quick_Python.run_query_commit(query, args)
