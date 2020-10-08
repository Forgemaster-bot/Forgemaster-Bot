import pyodbc
import Quick_Python
import Connections
from typing import List, Optional
from uuid import UUID


class Queries:
    """
    Container of static methods for handling player queries
    """
    @staticmethod
    def select_column(table_info, select_column: str) -> list:
        """
        Select database column by key
        :param table_info: table constants containing table definitions. Where table is table name, and key is table key
        :param select_column: column to get values from
        :return: dict containing database info
        """
        query = """\
                SELECT [{select_column}] 
                FROM [{table}]
                """.format(**table_info.to_dict(), select_column=select_column)
        cursor = Quick_Python.run_query(query, None)
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(row[0])
        return [] if not results else results

    @staticmethod
    def select(table_info, where_column: str, where_value: str,
               where_and_pairs: List[tuple] = None, order_by_column=None, ascending=True) -> List[dict]:
        """
        Select database row by key
        :param ascending:
        :param order_by_column:
        :param table_info: table constants containing table definitions. Where table is table name, and key is table key
        :param where_column: column to check for value
        :param where_value: where value
        :param where_and_pairs: pairs of key:value for adding to where clause
        :return: dict containing database info
        """
        if where_value == "*":
            where_query = ""
            args = None
        else:
            args = []
            if where_value is not None:
                where_query = f"WHERE [{where_column}] = ?"
                args.append(where_value)
            else:
                where_query = f"WHERE [{where_column}] IS NULL"

            if where_and_pairs is not None:
                keys, values = zip(*where_and_pairs)
                # add and items
                null_keys = []
                equals_keys = []
                for key, value in where_and_pairs:
                    if value is None:
                        null_keys.append(key)
                    else:
                        equals_keys.append(key)
                        args.append(value)
                where_and_items = [f"[{key}] = ?" for key in equals_keys]
                where_and_items.extend(f"[{key}] IS NULL" for key in null_keys)
                where_query = " AND ".join([where_query, *where_and_items])

        query = """\
                SELECT * 
                FROM [{table}]
                {where_query}
                """.format(**table_info.to_dict(), where_query=where_query)
        if order_by_column:
            query = f"{query} ORDER BY {order_by_column} {'ASC' if ascending else ''}"
        cursor = Quick_Python.run_query(query, args)

        # Convert cursor into dict with column as the key
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return [] if not results else results

    @staticmethod
    def update(table_info, data_info: dict, key_info: dict):
        # create set clause after splitting dictionary into keys and values
        data_keys = list(data_info.keys())
        data_values = list(data_info.values())
        set_clause = 'SET {}'.format(', '.join('[{}]=?'.format(k) for k in data_keys))

        # create where clause after splitting dictionary
        key_keys = list(key_info.keys())
        key_values = list(key_info.values())
        where_clause = 'WHERE {}'.format(' AND '.join('[{}]=?'.format(k) for k in key_keys))
        # add where_value to values for query
        for value in key_values:
            data_values.append(value)
        # Construct query and run it
        query = "UPDATE [{table}] {set_clause} {where_clause}".format(set_clause=set_clause,
                                                                      where_clause=where_clause,
                                                                      **table_info.to_dict())
        Quick_Python.run_query_commit(query, data_values)

    @staticmethod
    def insert(table_info, data: dict):
        # get column information for table attr of table_info
        column_data = Quick_Python.get_column_names_and_types(table_info.table)
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
                    values.append("?" if isinstance(arg, UUID) else "CONVERT(uniqueidentifier,?)")
                else:
                    values.append("NEWID()")
            else:
                args.append(arg)
                values.append('?')

        # Create column and value strings
        columns_string = ','.join("[{}]".format(k) for k in keys)
        values_string = ','.join(values)
        # output_string = "" if output is None else f"OUTPUT {', '.join(f'Inserted.{o}' for o in output)}"
        output_string = 'OUTPUT Inserted.*'
        query = f"INSERT INTO [{table_info.table}] ({columns_string}) {output_string} VALUES ({values_string})"

        # Quick_Python.run_query_commit(query, args)
        with Connections.sql_db_connection() as cursor:
            Quick_Python.log_transaction(query, args)
            cursor.execute(query, args)
            row = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))


    @staticmethod
    def delete(table_info, key_info: dict):
        # create where clause after splitting dictionary
        key_keys = list(key_info.keys())
        key_values = list(key_info.values())
        where_clause = 'WHERE {}'.format(' AND '.join('[{}]=?'.format(k) for k in key_keys))
        # create query
        query = "DELETE FROM [{table}] {where_clause}".format(**table_info.to_dict(), where_clause=where_clause)
        # run query
        Quick_Python.run_query_commit(query, key_values)
