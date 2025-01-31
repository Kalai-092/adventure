from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    # Connect to the SQLite database (it will create the file if it doesn't exist)
    with sqlite3.connect('database.db') as conn:
        # Create the contacts table if it doesn't exist
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

# Route to display the contact form and handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the contact information to the database
        with sqlite3.connect('database.db') as conn:
            conn.execute('''
                INSERT INTO contacts (name, email, message)
                VALUES (?, ?, ?)
            ''', (name, email, message))
            conn.commit()

        # After submission, redirect to a thank you page
        return redirect(url_for('thank_you'))

    # Display the form if GET request
    return render_template('index.html')

# Route to show a thank you message after form submission
@app.route('/thank-you')
def thank_you():
    return '<h1>Thank you for contacting us!</h1>'

# Main entry point to initialize the app and database
if __name__ == '__main__':
    init_db()  # Initialize the database (creates the table if not exists)
    app.run(debug=True)
