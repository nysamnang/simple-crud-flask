from flask import render_template, request, redirect, flash, url_for
from app import app
from models import User, Student, db
from forms import LoginForm, RegistrationForm, AddForm, UpdateForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', option='active'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or user.active == False:
            flash('Invalid username or password.', category='error')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', option='active')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, Now you can use your account for login!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/index')
def toindex():
    return redirect(url_for('index', option='active'))

@app.route('/index/<option>')
@login_required
def index(option):

    if option == 'active':
        return render_template(
            'index.html',
            student = Student.query.filter_by(active = True),
            view = 'active'
        )
    elif option == 'inactive':
        return render_template(
            'index.html',
            student = Student.query.filter_by(active = False),
            view = 'inactive'
        )

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddForm()
    student = Student.query.all()
    next_index = 0
    if len(student) == 0:
        next_index =1
    else:
        next_index = len(student) + 1
    
    if form.validate_on_submit():
        student = Student(
            student_id= u"MKT%s" % str(next_index),
            first_name_en = form.first_name_en.data,
            last_name_en = form.last_name_en.data,
            first_name_kh = form.first_name_kh.data,
            last_name_kh = form.last_name_kh.data,
            gender = form.gender.data,
            date_of_birth = form.date_of_birth.data,
            phone = form.phone.data,
            email = form.email.data,
            address = form.address.data
        )
        db.session.add(student)
        db.session.commit()

        flash('Student has been registered successfuly!', category='success')
        return redirect(url_for('index', option='active'))
    return render_template('add_student.html', form=form)

@app.route('/update_student/<student_id>', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    form = UpdateForm()
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    if form.validate_on_submit():

        student.student_id=student_id,
        student.first_name_en = form.first_name_en.data,
        student.last_name_en = form.last_name_en.data,
        student.first_name_kh = form.first_name_kh.data,
        student.last_name_kh = form.last_name_kh.data,
        student.gender = form.gender.data,
        student.date_of_birth = form.date_of_birth.data,
        student.phone = form.phone.data,
        student.email = form.email.data,
        student.address = form.address.data

        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('index', option='active'))
    elif request.method == 'GET':
        form.student_id.data = student.student_id
        form.first_name_en.data = student.first_name_en
        form.last_name_en.data = student.last_name_en
        form.first_name_kh.data = student.first_name_kh
        form.last_name_kh.data = student.last_name_kh
        form.gender.data = student.gender
        form.date_of_birth.data = student.date_of_birth
        form.phone.data = student.phone
        form.email.data = student.email
        form.address.data = student.address

    return render_template('update_student.html', form=form)

@app.route('/delete_student/<student_id>')
@login_required
def delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    student.active = False
    # db.session.delete(student)
    db.session.commit()
    return redirect('index')

@app.route('/undo_delete_student/<student_id>')
@login_required
def undo_delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    student.active = True
    db.session.commit()
    return redirect('index')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
