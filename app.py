from flask import Flask, request, render_template, url_for, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = '2.zdz0X`;U31#ow3!IH[GfG`uSnvSls;,"%oI*%3h_KLbq0n?k|#/:K"?kz9<}.'


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
    adminStatus = True
    return render_template("home.html", classes=get_classes(), ordinals=ordinals, adminStatus=adminStatus)

    
@app.route('/login')
def login():
    if "username" not in session:
        return render_template("login.html")

    
def user_exists(username, password):
    conn = get_db_connection()
    
    result = conn.execute("SELECT user_id FROM users WHERE username='%s' AND PASSWORD='%s'" % (username, password))
    user_id = result.fetchone()[0]
    
    result = conn.execute("SELECT username FROM users WHERE username='%s' AND PASSWORD='%s' AND user_id=%d" % (username, password, user_id))

    if result is not None:
        return True
    else: 
        return False
    #Addd functiont o check if user exists, other wise deny access
    
def create_user(username, password, hierarchy):
    conn = get_db_connection()
    
    if (user_exists != True):
        result = conn.execute("INSERT INTO users (username, password, hierarchy) VALUES (?, ?, ?)", (username, password, hierarchy))
        conn.commit()
        conn.close()
    else:
        return "User already exists"
    
    conn.close()

def delete_user(username, password):
    conn = get_db_connection()
    
    result = conn.execute("SELECT user_id FROM users WHERE username='%s' AND PASSWORD='%s'" % (username, password))
    user_id = result.fetchone()[0]
    
    conn.execute("DELETE FROM users WHERE user_id = %d AND username = '%s' AND password='%s'" % (user_id, username, password))

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
        
        if (firstname == None or lastname == None or grade == None or o1 == None or o2 == None or o3 == None or o4 == None or o5 == None):
            return "You must fill out ALL information"

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (firstname, lastname) VALUES (?, ?)', (firstname, lastname))

        conn.commit()
        conn.close()
        userStatus = True
        
        return render_template("completed.html", status=userStatus, firstname=firstname, lastname=lastname, grade=grade, o1=o1, o2=o2, o3=o3, o4=o4, o5=o5)
        
    else:
        return "Invalid action, return to last page", 400

@app.errorhandler(404)
def pnf(placeholder):
    return render_template("pnf.html")

if __name__ == "__main__":
    app.run(debug=True)
