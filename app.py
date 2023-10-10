from flask import Flask, request, render_template, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'fsdajlkjalasjlfdslj'


@app.route("/")
def startingPage():
    return render_template('home.html')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/completed", methods=["POST", "GET"])
def Userinputs():

    if request.method == "POST":
        firstname = request.form.get('First Name')
        lastname = request.form.get('Last Name')

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (firstname, lastname) VALUES (?, ?)', (firstname, lastname))

        conn.commit()
        conn.close()


    return render_template('completed.html')


if __name__ == "__main__":
    app.run(debug=True)
