from flask import Flask
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello_world():
    connector = sqlite3.connect("my-test.db")
    new_line = '\n'
    with connector:
        resp = connector.execute("SELECT * FROM USAGES JOIN USER_ACTIONS UA on USAGES.action = UA.id ").fetchall()
    answer = ""
    for row in resp:
        answer += new_line.join([str(element) for element in row])
    return f"<p>Hello, World!</p><div>{answer}</div>"
