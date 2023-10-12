from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'fs214353daj23lkj341al3124asj48u231o812u4o1l4312fds43lj'


def get_classes():
    classes = set()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    table = cur.execute('SELECT * FROM classes')
    for row in table:
        classes.add(row[2])
    return classes


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def starting_page():
    ordinals = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
    return render_template('home.html', classes=get_classes(), ordinals=ordinals)


@app.route("/completed", methods=["POST", "GET"])
def user_inputs():
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
