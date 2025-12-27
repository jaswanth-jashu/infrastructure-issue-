from flask import Flask, render_template, request
import sqlite3
import uuid
from flask_mail import Mail, Message

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'k.tejeshtejesh@gmail.com'
app.config['MAIL_PASSWORD'] = 'heym bvbe zunt yrvo'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        area = request.form['area']
        street = request.form['street']
        issue = request.form['issue']
        email = request.form['email']

        reference_id = "SC-" + str(uuid.uuid4())[:8]

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO issues (reference_id, city, area, street, issue, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (reference_id, city, area, street, issue, "Submitted"))
        conn.commit()
        conn.close()

        msg = Message(
            'Issue Report Confirmation',
            sender='your_email@gmail.com',
            recipients=[email]
        )
        msg.body = f"""
Your issue has been successfully reported.

Reference ID: {reference_id}
Issue: {issue}
Location: {street}, {area}, {city}

Thank you for helping improve the city.
"""
        mail.send(msg)

        return f"Issue submitted successfully! Reference ID: {reference_id}"

    return render_template('index.html')
@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT reference_id, city, area, street, issue, status FROM issues")
    issues = cursor.fetchall()

    conn.close()

    return render_template('admin.html', issues=issues)


if __name__ == '__main__':
    app.run(debug=True)