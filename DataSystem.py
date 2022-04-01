import sqlite3 as sl
import time


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


class UserLogs:
    def __init__(self):
        self.con = sl.connect('my-test.db')

    def activate(self):
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

    def add_log(self, user, action):
        with self.con:
            data = self.con.execute("SELECT COUNT(*) FROM USER_ACTIONS WHERE action_name=?", (action))
            if data is None:
                self.con.execute("INSERT INTO USER_ACTIONS (action_name) values(?)", (action))
                data = data = self.con.execute("SELECT COUNT(*) FROM USER_ACTIONS WHERE action_name=?", (action))

            sql = 'INSERT INTO USAGES (time, user, action) values(?, ?, ?)'
            self.con.execute(sql, (time.time(), user, data[0]))


UserLogs().activate()
