import sqlite3 as sl
from controls.settings import DATA_BASE


class DataBaseConnector(object):

    def __new__(cls, database_name, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataBaseConnector, cls).__new__(cls)
            cls.instance.con = sl.connect(database_name)
        return cls.instance


class AbstractModel(object):
    def __init__(self):
        self.con = DataBaseConnector(DATA_BASE).con
        self.con.row_factory = sl.Row

    @classmethod
    def get_data(cls, func):
        def wrap(self):
            r = []
            plate = type(self)
            for result in func(self).fetchall():
                temp = plate()
                for key_num in range(len(result.keys())):
                    setattr(temp, result.keys()[key_num], result[key_num])
                r.append(temp)
            return r
        return wrap

    def __create__(self):
        raise NotImplementedError
