from flask import Flask
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    connector = sqlite3.connect("my-test.db")
    new_line = '<br>>'
    with connector:
        resp = connector.execute("SELECT * FROM USAGES JOIN USER_ACTIONS UA on USAGES.action = UA.id ").fetchall()
    answer = ""
    for row in resp:
        answer += new_line.join([str(element) for element in row])
    return f"<p>Hello, World!</p><div>{answer}</div>"


@app.route("/ls")
def ls():
    import os

    arr = os.listdir()
    return " ".join(arr)


if __name__ == '__main__':
    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = os.environ.get('PORT')

    if port:
        # 'PORT' variable exists - running on Heroku, listen on external IP and on given by Heroku port
        app.run(host='0.0.0.0', port=int(port))
    else:
        # 'PORT' variable doesn't exist, running not on Heroku, presumabely running locally, run with default
        #   values for Flask (listening only on localhost on default Flask port)
        app.run()
