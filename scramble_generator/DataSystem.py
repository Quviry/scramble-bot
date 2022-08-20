import sqlite3 as sl
import time
from engine.models.models import AbstractModel


def log_user_action(user, action):
    con = sl.connect('my-test.db')
    with con:
        con.execute("""
                CREATE TABLE IF NOT EXISTS USAGES (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    time DATETIME,
                    user TEXT,
                    action INTEGER
                );""")
        con.execute("""                 
                CREATE TABLE IF NOT EXISTS USER_ACTIONS (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    action_name TEXT,
                    FOREIGN KEY(id) REFERENCES USAGES(action)
                );
            """)
    with con:
        data = con.execute("SELECT COUNT(*) FROM USER_ACTIONS WHERE (action_name=?);", [action]).fetchone()
        if data[0] == 0:
            con.execute("INSERT INTO USER_ACTIONS (action_name) values(?);", [action])
        if data[0] > 1:
            raise Exception("TOTL PIZDTS")
        data = con.execute("SELECT id FROM USER_ACTIONS WHERE action_name=?;", [action]).fetchone()

        sql = 'INSERT INTO USAGES (time, user, action) values(?, ?, ?)'
        con.execute(sql, (time.time(), user, data[0],))


class UserLogs(AbstractModel):
    id: int
    time: float
    user: str
    action: int

    def __create__(self):
        with self.con:
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS USAGES (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    time DATETIME,
                    user TEXT,
                    action INTEGER
                );""")
            self.con.execute("""                 
                CREATE TABLE IF NOT EXISTS USER_ACTIONS (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    action_name TEXT,
                    FOREIGN KEY(id) REFERENCES USAGES(action)
                );
            """)

    @AbstractModel.get_data
    def get_all(self):
        with self.con:
            return self.con.execute("""SELECT * FROM USAGES;""")

    def add_log(self, user, action):
        with self.con:
            data = self.con.execute("SELECT COUNT(*) FROM USER_ACTIONS WHERE action_name=?", [action]).fetchone()
            if data is None:
                self.con.execute("INSERT INTO USER_ACTIONS (action_name) values(?)", [action])
                data = self.con.execute("SELECT COUNT(*) FROM USER_ACTIONS WHERE action_name=?", [action]).fetchone()

            sql = 'INSERT INTO USAGES (time, user, action) values(?, ?, ?)'
            self.con.execute(sql, (time.time(), user, data[0]))

    def __str__(self):
        return f"<UserLogs id={self.id}>"

    def __repr__(self):
        if self.id is None:
            _id = -1
        else:
            _id = self.id
        return f"<UserLogs id={_id}>"


a = UserLogs()
# a.__create__()
print(a.get_all())
