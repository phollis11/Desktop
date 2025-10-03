from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
import sqlite3
import os

#develop this with react 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
DB_FILE = 'forms.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
            #is_admin uses 0 for not admin and 1 for admin
            #privelages idea, if users(is_admin) == 1 show html for admin page, otherwise show normal users page
            #going to use TEXT (True) or (False) first for simplicity
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL
        )
        '''
        )
        #make a seperate page for becoming an admin once you create an account. This is should be much simpler than doing so at registration

        #status idea, if STATUS == 0 not responded too, if STATUS == 1 in progress, if statues == 2 completed

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets(
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            urgency TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)     
        )
        '''
        )

        conn.commit()


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute(
            "SELECT * FROM tickets WHERE user_id = ? ORDER BY date DESC",
            (session['user_id'],)
        ).fetchall()
    return render_template('index.html', tickets=rows, user_email=session.get('email'), is_admin = session.get('is_admin'))

@app.route('/admin')
def admin_home():
    if 'user_id' not in session:
        return redirect('/login')

    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute(
            "SELECT * FROM tickets Order By date DESC"
        ).fetchall()
    return render_template('admin_index.html', tickets=rows, user_email=session.get('email'), is_admin = session.get('is_admin'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        with sqlite3.connect(DB_FILE) as conn:
                try:
                    conn.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)", (name,email, password, 0))
                    conn.commit()
                    flash('Registration successful. Please log in.', 'success')
                    return redirect('/login')
                except sqlite3.IntegrityError:
                    flash('Email already registered.', 'error')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect(DB_FILE) as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password)
            ).fetchone()

            if user:
                session['user_id'] = user[0]
                session['email'] = user[2]
                session['password'] = user[3]
                session['is_admin'] = int(user[4])

                is_admin = user[4]
                if is_admin == 1:
                    return redirect('/admin')

                print("Login successful: Redirecting to /")
                return redirect('/')
            else:
                flash('Invalid credentials. Please try again.', 'error')
                print("Login failed: wrong credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods =['POST'])
def add_ticket():
    if 'user_id' not in session:
        return redirect('/login')
    
    date = str(datetime.now())
    status = "No Response"

    data = (
        #ticket_id autoincrements
        session['user_id'], #get user_id
        request.form['location'], #location given by user
        request.form['urgency'], #urgency given by user, could also change to catgegory and urgency given based on category
        request.form['description'], #description given by user
        date, 
        status
        
    )

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO tickets (user_id, location, urgency, description, date, status) VALUES (?, ?, ?, ?, ?, ?)",
            data
        )
    
    return redirect('/')


@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == "POST":
        email = session.get('email')
        pin = request.form.get('pin')
        admin_pin = "123"

        if not email:
            flash("Session expired. Please log in again.")
            return redirect('/login')

        if admin_pin == pin:
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    print(f"[DEBUG] session email: {email}")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", (email,))
                    conn.commit()

                    print(f"Rows updated: {cursor.rowcount}")
                    if cursor.rowcount == 0:
                        flash("Admin update failed: email not found.")
                        return redirect('/admin_register')

                session['is_admin'] = 1
                flash("You are now an admin.")
                return redirect('/admin')
            except Exception as e:
                print(f"DB Error: {e}")
                flash("Database error.")
                return redirect('/admin_register')
        else:
            flash("Incorrect admin pin.")
            return redirect('/admin_register')

    return render_template('admin_register.html')

@app.route('/update_status', methods=['POST'])
def update_status():
    if session.get('is_admin') != 1:
        flash("Access denied.")
        return redirect('/')

    ticket_id = request.form.get('ticket_id')
    new_status = request.form.get('new_status')

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "UPDATE tickets SET status = ? WHERE ticket_id = ?",
            (new_status, ticket_id)
        )
        conn.commit()

    flash(f"Ticket {ticket_id} updated to '{new_status}'")
    return redirect('/admin')

@app.route('/respond', methods=['POST'])
def respond():
    if session.get('is_admin') !=1:
        flash("Access denied.")
        return redirect('/')
    
    ticket_id = request.form.get('ticket_id')
    timeframe = request.form.get('timeframe')

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "UPDATE tickets SET status = ? WHERE ticket_id = ?", (timeframe, ticket_id)
        )
        conn.commit()
        return redirect('/admin')







if __name__ == '__main__':
    init_db()
    app.run(debug=True)