from Character.Tables.Queries import Queries
class InfoMaxSpellLevel:
    """
    Static data holder for the Info_Max_Spell_Level database. Since data is static, this will be used to save some queries
    """
    _data = None

    class TableInfo:
        table = 'Info_Max_Spell_Level'
        key = 'Class'

        @classmethod
        def to_dict(cls) -> dict:
            return {'table': cls.table}

    @classmethod
    def _fetch_data(cls):
        rows = Queries.select(cls.TableInfo, None, "*")
        data = {}
        for row in rows:
            key = row.pop(cls.TableInfo.key)
            data[key] = {}
            for level, value in row.items():
                level = level.replace('level_', '')
                level = int(level)
                data[key][level] = value
        return data

    @classmethod
    def get_data(cls):
        if cls._data is None:
            cls._data = cls._fetch_data()
        return cls._data
