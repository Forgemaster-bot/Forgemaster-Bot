from typing import List
from Quick_Python import transform_dict_keys
import ast


class TableMapper:
    """
    CharacterInfo info storage
    """
    def __init__(self, queries, table_info, storage_type):
        """
        Define dependency injection objects
        :param queries:
        :param table_info:
        :param storage_type:
        """
        self._queries = queries
        self._table_info = table_info
        self._storage_type = storage_type

    def fetch(self, value, column=None, where_and_pairs=None) -> List:
        """
        Fetch CharacterClass objects from tables using _table_info.key as key
        :param value: value to use for fetching data from key column in tables
        :param column: column to search
        :param where_and_pairs: extra pairs to pass to select call
        :return: List of CharacterClass objects
        """
        where_column = self._table_info.key if column is None else column
        table_dicts = self._queries.select(self._table_info, where_column, value, where_and_pairs)
        storage_obj_list = []
        for row_dict in table_dicts:
            transformed_dict = transform_dict_keys(row_dict, self._table_info.to_column_dict())
            storage_obj_list.append(self._storage_type(**transformed_dict))
        return storage_obj_list

    def fetch_keys(self) -> list:
        """
        Fetch keys objects from table using _table_info.key
        :return: List of values
        """
        return self._queries.select_column(self._table_info, self._table_info.key)

    def update(self, storage_obj) -> None:
        data = transform_dict_keys(storage_obj.to_dict(), self._table_info.to_dict())
        # where_info = {k: data.pop(k) for k in self._table_info.update_keys}
        where_info = {}
        for k in ast.literal_eval(self._table_info.update_keys):
            where_info[k] = data.pop(k)
        if not data:
            raise RuntimeError('Cannot update data passed. No allowable columns to set.')
        self._queries.update(self._table_info, data, where_info)

    def insert(self, storage_obj) -> None:
        query_dict = transform_dict_keys(storage_obj.to_dict(), self._table_info.to_dict())
        self._queries.insert(self._table_info, query_dict)

    def delete(self, storage_obj) -> None:
        data = transform_dict_keys(storage_obj.to_dict(), self._table_info.to_dict())
        where_info = {}
        for k in ast.literal_eval(self._table_info.update_keys):
            where_info[k] = data.pop(k)
        self._queries.delete(self._table_info, where_info)

    @property
    def table_info(self):
        return self._table_info

    @table_info.setter
    def table_info(self, value):
        self._table_info = value

    @property
    def storage_type(self):
        return self._storage_type

    @storage_type.setter
    def storage_type(self, value):
        self._storage_type = value
