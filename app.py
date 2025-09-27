from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from flask_mail import Mail, Message
from datetime import timedelta

app = Flask(__name__)

# Secret key for session
app.secret_key = "your_secret_key"

# Session lifetime
app.permanent_session_lifetime = timedelta(minutes=30)

# MySQL connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='portfolio_db'
)

cursor = db.cursor(dictionary=True)

# ----- Flask-Mail Config -----
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jones936112@gmail.com'
app.config['MAIL_PASSWORD'] = '@Jones#0612'   # ⚠️ Use Gmail App Password, not your real password

mail = Mail(app)


# ---------------- HOME ----------------
@app.route('/')
def home():
    cursor.execute("SELECT * FROM project_status")
    projects = cursor.fetchall()

    # load skills for homepage
    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()

    # convert into category → skills mapping
    skill_categories = {}
    for skill in skills:
        category = skill['category']
        if category not in skill_categories:
            skill_categories[category] = []
        skill_categories[category].append(skill)  # full skill dict

    return render_template(
        'index.html',
        skill_categories=skill_categories,
        projects=projects
    )


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):  # Already logged in
        return redirect(url_for('admin'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    

    # -------- Statistics --------
    # -------- Project Statistics from project_status --------
    cursor.execute("SELECT COUNT(*) AS total_projects FROM project_status")
    total_projects = cursor.fetchone()['total_projects']

    cursor.execute("SELECT COUNT(*) AS completed FROM project_status WHERE status='completed'")
    completed_projects = cursor.fetchone()['completed']

    cursor.execute("SELECT COUNT(*) AS ongoing FROM project_status WHERE status='ongoing'")
    ongoing_projects = cursor.fetchone()['ongoing']

    cursor.execute("SELECT COUNT(DISTINCT client_name) AS clients FROM project_status")
    clients = cursor.fetchone()['clients']

    # Skills statistics
    cursor.execute("SELECT COUNT(DISTINCT category) AS technologies FROM skills")
    technologies_used = cursor.fetchone()['technologies']

    project_statistics = {
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "ongoing_projects": ongoing_projects,
        "clients": clients,
        "technologies_used": technologies_used
    }

    return render_template(
        "admin.html",
        project_statistics=project_statistics
    )


# ---------------- ADD PROJECT ----------------
@app.route('/admin/add_project', methods=['GET', 'POST'])
def add_project():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        link = request.form.get('link', '')
        client_name = request.form.get('client_name', '')
        status = request.form.get('status', 'ongoing')

        cursor.execute("""
            INSERT INTO project_status (project_title, description, link, status, client_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, link, status, client_name))
        db.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for('add_project'))

    cursor.execute("SELECT * FROM project_status ORDER BY created_at DESC")
    projects = cursor.fetchall()
    return render_template('add_project.html', projects=projects)

# ---------------- UPDATE PROJECT ----------------
@app.route('/admin/project_update/<int:id>', methods=['GET', 'POST'])
def project_update(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM project_status WHERE id=%s", (id,))
    project = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        link = request.form.get('link', '')
        client_name = request.form.get('client_name', '')
        status = request.form.get('status', 'ongoing')

        cursor.execute("""
            UPDATE project_status 
            SET project_title=%s, description=%s, link=%s, status=%s, client_name=%s
            WHERE id=%s
        """, (title, description, link, status, client_name, id))
        db.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for('add_project'))

    return render_template('edit_project.html', project=project)

# ---------------- DELETE PROJECT ----------------
@app.route('/admin/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM project_status WHERE id=%s", (id,))
    db.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for('add_project'))


# ---------------- SKILLS ----------------
# Add new skill
@app.route('/admin/add_skill', methods=['GET', 'POST'])
def add_skill():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        icon_class = request.form['icon_class']
        description = request.form['description']
        proficiency_level = request.form['proficiency_level']
        proficiency_percent = int(request.form['proficiency_percent'])

        cursor.execute(
            "INSERT INTO skills (category, name, icon_class, description, proficiency_level, proficiency_percent) VALUES (%s,%s,%s,%s,%s,%s)",
            (category, name, icon_class, description, proficiency_level, proficiency_percent)
        )
        db.commit()
        return redirect(url_for('add_skill'))
    
    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()
    return render_template('add_skills.html', skills=skills)


# Edit skill
@app.route('/admin/edit_skill/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM skills WHERE id=%s", (skill_id,))
    skill = cursor.fetchone()

    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        icon_class = request.form['icon_class']
        description = request.form['description']
        proficiency_level = request.form['proficiency_level']
        proficiency_percent = int(request.form['proficiency_percent'])

        cursor.execute("""
            UPDATE skills 
            SET category=%s, name=%s, icon_class=%s, description=%s, proficiency_level=%s, proficiency_percent=%s 
            WHERE id=%s
        """, (category, name, icon_class, description, proficiency_level, proficiency_percent, skill_id))
        db.commit()
        return redirect(url_for('add_skill'))

    return render_template('edit_skill.html', skill=skill)


# Delete skill
@app.route('/admin/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM skills WHERE id=%s", (skill_id,))
    db.commit()
    return redirect(url_for('add_skill'))


# ----- Contact Page -----
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # 1️⃣ Save to database
        sql = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        db.commit()

        # 2️⃣ Send Email to Admin
        try:
            msg = Message(subject=f"New Contact Message from {name}",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['your_real_email@gmail.com'],  # CHANGE THIS
                          body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}")
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", e)

        flash("Message submitted successfully!", "success")
        return redirect(url_for('contact'))

    # 🔹 fetch projects + skills again for index.html
    cursor.execute("SELECT * FROM project")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()

    skill_categories = {}
    for skill in skills:
        category = skill['category']
        if category not in skill_categories:
            skill_categories[category] = []
        skill_categories[category].append(skill)

    return render_template("index.html", projects=projects, skill_categories=skill_categories)


# ----- Admin Dashboard Messages -----
@app.route('/admin/messages')
def admin_messages():
    cursor.execute("SELECT * FROM contact_messages ORDER BY id DESC")
    messages = cursor.fetchall()
    return render_template("admin_messages.html", messages=messages)


# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(debug=True)
