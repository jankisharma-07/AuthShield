from flask import Flask, render_template, request, redirect, session, jsonify
from password_checker import check_password_details, suggest_password
from brute_force_detector import record_attempt, is_suspicious, reset_attempts, lock_account, is_locked, locked_accounts
import database
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"  

# 🔐 LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    remaining_time = 0

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        #  Check lock
        if is_locked(username):
            remaining_time = int(locked_accounts[username] - time.time())
            message = "Account Locked!"
            return render_template('login.html', message=message, remaining_time=remaining_time)

        # Check credentials
        database.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = database.cursor.fetchone()

        if user:
            reset_attempts(username)
            session['username'] = username

            # Log success
            database.cursor.execute(
                "INSERT INTO logs(username,status,ip) VALUES (?,?,?)",
                (username, 'SUCCESS', ip)
            )
            database.conn.commit()

            return redirect('/dashboard')
        else:
            record_attempt(username)

            # Log failed attempt
            database.cursor.execute(
                "INSERT INTO logs(username,status,ip) VALUES (?,?,?)",
                (username, 'FAILED', ip)
            )
            database.conn.commit()

            if is_suspicious(username):
                lock_account(username)
                remaining_time = 30
                message = "Too many attempts! Account locked."
            else:
                message = "Wrong Username or Password"

    return render_template('login.html', message=message, remaining_time=remaining_time)


#  DASHBOARD
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect('/')

    database.cursor.execute("SELECT * FROM logs WHERE username=? ORDER BY time DESC", (username,))
    logs = database.cursor.fetchall()
    return render_template('dashboard.html', logs=logs)


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""
    errors = []
    username = ""

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Check password errors
        errors = check_password_details(password)
        if errors:
            return render_template('signup.html', errors=errors, message="", username=username)

        #  Check duplicate username
        database.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if database.cursor.fetchone():
            message = "User already exists!"
            return render_template('signup.html', errors=[], message=message, username=username)

        # Insert new user
        database.cursor.execute("INSERT INTO users (username,password) VALUES (?, ?)", (username, password))
        database.conn.commit()
        message = "Signup Successful!"
        return render_template('signup.html', errors=[], message=message, username="")

    # GET request
    return render_template('signup.html', errors=[], message="", username="")


#  Suggest password route (AJAX)
@app.route('/suggest_password')
def suggest_password_route():
    suggested = suggest_password()
    return jsonify({"password": suggested})


if __name__ == '__main__':
    app.run(debug=True)