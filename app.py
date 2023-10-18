from flask import Flask, request, render_template, url_for, session, redirect
import sqlite3
from init_db import init_db

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

@app.route("/schedule-management")
def schedule_management():
    if "username" in session:
        adminStatus = True
        classes = get_classes()
        ordinals = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
        return render_template("schedule-management.html", classes=classes, ordinals=ordinals, adminStatus=adminStatus)

    else:
        session['loginStatus'] = "Login to create Tasks"
        return redirect("/login")
    
@app.route("/")
def home():
    return render_template("home.html")

    
@app.route('/login', methods=['POST', 'GET'])
def login():
    #Fix this hole shit hole
    if "username" in session:
        username = session["username"]
        return redirect("/profile")
    
    else:
        if request.method == "POST":
            if "username" in request.form and "password" in request.form:
                username = request.form.get('username')
                password = request.form.get('password')
        
                if user_exists(username, password):
                    session.pop("loginStatus", None)
                    session["username"] = username
                    return redirect("/profile")
                else:
                    return "User does not exist, go to sign up page", 400
            
            else:
                return render_template("login.html", code="302")
            
        else:
            return render_template("login.html")
        
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if "username" in session:
        username = request.form.get('username')
        session["username"] = username
        return redirect("/profile")
    
    else: 
        if request.method == "POST":
            if "username" in request.form and "password" in request.form and "school" in request.form:
                username = request.form.get('username')
                password = request.form.get('password')
                school = request.form.get('school')
                
                if user_exists(username, password):
                    return "User already exists, go to login page", 400
                else:
                    if "hierarchy" in request.form:
                        hierarchy = request.form.get('hierarchy')
                        create_user(username, password, hierarchy, school)
                        session["username"] = username
                        
                        return redirect('/profile', code=300)
                    
                    else:
                        return render_template("signup.html")
            else:
                return render_template("signup.html")
        
        else:
            return render_template("signup.html")  
            
@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
                               
    
def user_exists(username, password):
    conn = get_db_connection()
    
    result = conn.execute("SELECT username FROM users WHERE username='%s' AND PASSWORD='%s'" % (username, password))
    return result.fetchone() is not None

    
def create_user(username, password, hierarchy, school):
    conn = get_db_connection()
    
    result = conn.execute("INSERT INTO users (username, password, hierarchy, school) VALUES (?, ?, ?, ?)", (username, password, hierarchy, school))
    conn.commit()
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
