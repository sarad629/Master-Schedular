from flask import Flask, request, render_template, url_for
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
        
        grade = request.form["Grade"]
        o1 = request.form["First Choice"]
        o2 = request.form["Second Choice"]
        o3 = request.form["Third Choice"]
        o4 = request.form["Fourth Choice"]
        o5 = request.form["Fifth Choice"]

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (firstname, lastname) VALUES (?, ?)', (firstname, lastname))

        conn.commit()
        conn.close()
        userStatus = True
        
    else:
        return "Invalid action, return to last page", 400

    return render_template('completed.html', status=userStatus, firstname=firstname, lastname=lastname, grade=grade, o1=o1, o2=o2, o3=o3, o4=o4, o5=o5)

@app.errorhandler(404)
def pnf(placeholder):
    return render_template('pnf.html')

if __name__ == "__main__":
    app.run(debug=True)
