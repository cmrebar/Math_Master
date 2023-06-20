from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
import mathgenerator as mg
import random
import math
bcrypt = Bcrypt(app)

def closest_larger_multiple(number):
    quotient, remainder = divmod(number, 50)
    if remainder == 0:
        return number
    else:
        closest_multiple = (quotient + 1) * 50
        return closest_multiple
    
def remove_duplicates(array):
    seen = set()
    for i in (range(len(array) - 1)):
        if array[i] in seen:
            duplicate = array[i]
            array.remove(duplicate)
        else:
            seen.add(array[i])
    return array

@app.route('/')
def index():
    if not 'user_id' in session:
        flash('You must login to continue')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def create_user ():
    if not User.validate_user(request.form):
        
        return redirect('/')
    data = { 'email' : request.form['email'] }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash('Email already in use')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
        'tracked_points' : request.form['tracked_points']
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
    user = User.get_by_id(user_data)
    milestone = closest_larger_multiple(user.tracked_points)
    milestones = user.hidden_points / 50
    user.milestones = math.floor(milestones)
    data = {
        'id' : user.id,
        'milestones' : user.milestones,
        'tracked_points' : user.tracked_points,
        'hidden_points' : user.hidden_points
    }
    User.update_points(data)
    user = User.get_by_id(user_data)
    return render_template('dashboard.html', user = user, milestone = milestone, users = User.getAll())

@app.route('/problems/<id>')
def view_problem(id):
    session['problem_id'] = id
    problem_id = int(id)
    problem, solution = mg.genById(problem_id)
    _, wrong1 = mg.genById(problem_id)
    _, wrong2 = mg.genById(problem_id)
    _, wrong3 = mg.genById(problem_id)
    options = [solution, wrong1, wrong2, wrong3]
    if options[0] == "Yes":
        options[1] = "No"
        options.remove(wrong2)
        options.remove(wrong3)
    elif options[0] == "No":
        options[1] = "Yes"
        options.remove(wrong2)
        options.remove(wrong3)
    else:
        pass
    options = remove_duplicates(options)
    random.shuffle(options)

    user_data = { 'id' : session['user_id']}
    user = User.get_by_id(user_data)
    milestone = closest_larger_multiple(user.tracked_points)
    return render_template("problems.html", problem=problem, options=options, solution=solution, user = user, milestone = milestone, users = User.getAll())

@app.route('/problems/check', methods=['POST'])
def check_answer():
    user_data = { 'id' : session['user_id']}
    user = User.get_by_id(user_data)
    id = session['problem_id']
    if request.form['user_solution'] == request.form['solution']:
        user.tracked_points = user.tracked_points + 1
        user.hidden_points = user.hidden_points + 1
        milestones = user.hidden_points / 50
        user.milestones = math.floor(milestones)
        data = {
            'id' : user.id,
            'tracked_points' : user.tracked_points,
            'hidden_points' : user.hidden_points,
            'milestones' : user.milestones
        }
        User.update_points(data)
        flash('Correct!', 'correct')
        return redirect('/problems/' + id)
    else:
        flash('Incorrect!', 'incorrect')
        return redirect('/problems/' + id)
    
@app.route('/rewards')
def rewards():
    user_data = { 'id' : session['user_id']}
    user = User.get_by_id(user_data)
    milestone = closest_larger_multiple(user.tracked_points)
    return render_template('rewards.html', user = user, milestone = milestone, users = User.getAll())

@app.route('/rewards/<title>')
def claim_reward(title):
    print('GOTCHA')
    user_data = { 'id' : session['user_id']}
    user = User.get_by_id(user_data)
    if user.milestones < 1:
        flash('You do not have enough milestones to claim this reward! (You get 1 milestone for every 25 points you earn.))')
        return redirect('/rewards')
    else:
        user.milestones = user.milestones - 1
        user.hidden_points = user.hidden_points - 50
        data = {
            'id' : user.id,
            'milestones' : user.milestones,
            'title' : title,
            'hidden_points' : user.hidden_points
        }
        User.update_title(data)
        print('GOTCHA2')
        flash('Reward claimed!')
        return redirect('/rewards')