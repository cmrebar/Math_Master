from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
import mathgenerator as mg
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if not 'user_id' in session:
        flash('You must login to continue')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def create_user ():
    if not User.validate_user(request.form):
        
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
        'points' : request.form['points']
    }
    user_id = User.save(data)
    print(user_id)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods=['POST'] )
def login():
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        print(user_in_db)
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print(bcrypt.generate_password_hash(request.form['password']))
        print(user_in_db.password)
        flash('Invalid Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    user_data = { 'id' : session['user_id']}
    return render_template('dashboard.html', user = User.get_by_id(user_data))

@app.route('/problems/<id>')
def view_problem(id):
    problem_id = int(id)
    problem, solution = mg.genById(problem_id)
    _, wrong1 = mg.genById(problem_id)
    _, wrong2 = mg.genById(problem_id)
    _, wrong3 = mg.genById(problem_id)
    user_data = { 'id' : session['user_id']}
    print(problem, solution)
    return render_template("problems.html", problem=problem, solution=solution, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3, user = User.get_by_id(user_data), users = User.getAll())