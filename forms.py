# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, Optional
from models import User, Student
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=15), Regexp('^[a-zA-Z]*$', message="Please enter characters A-Z only.")])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist.')

class AddForm(FlaskForm):
    REGEX_ENGLISH = "^[a-zA-Z ]*$"
    REGEX_KHMER = u"^[\u1780-\u17FF ]*$"
    REGEX_PHONE = "^[0-9]*$"

    student_id = StringField()
    first_name_en = StringField(validators=[DataRequired(), Length(max=15), Regexp(REGEX_ENGLISH, message="Please enter characters A-Z only.")])
    last_name_en = StringField(validators=[DataRequired(), Length(max=15), Regexp(REGEX_ENGLISH, message="Please enter characters A-Z only.")])
    first_name_kh = StringField(validators=[Optional(), Length(max=15), Regexp(REGEX_KHMER, message="Please enter Khmer letters only.")])
    last_name_kh = StringField(validators=[Optional(), Length(max=15), Regexp(REGEX_KHMER, message="Please enter Khmer letters only.")])
    gender = RadioField('Gender',choices=[('M','Male'),('F','Female'),('O','Other')], default='F', validators=[DataRequired()])
    date_of_birth = StringField(validators=[DataRequired(), Length(max=10)])
    phone = StringField(validators=[DataRequired(), Length(min=9, max=10), Regexp(REGEX_PHONE, message="Please enter number only.")])
    email = StringField(validators=[Optional(), Length(max=50), Email()])
    address = StringField(validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Register')

    def validate_date_of_birth(self, date_of_birth):
        birth_date = datetime.strptime(date_of_birth.data, '%Y-%m-%d')
        age = int((datetime.today() - birth_date).days/365.2425)

        if age < 18:
            raise ValidationError('Age must be at least 18 years old.')


class UpdateForm(FlaskForm):
    REGEX_ENGLISH = "^[a-zA-Z ]*$"
    REGEX_KHMER = u"^[\u1780-\u17FF ]*$"
    REGEX_PHONE = "^[0-9]*$"

    student_id = StringField()
    first_name_en = StringField(validators=[DataRequired(), Length(max=15), Regexp(REGEX_ENGLISH, message="Please enter characters A-Z only.")])
    last_name_en = StringField(validators=[DataRequired(), Length(max=15), Regexp(REGEX_ENGLISH, message="Please enter characters A-Z only.")])
    first_name_kh = StringField(validators=[Optional(), Length(max=15), Regexp(REGEX_KHMER, message="Please enter Khmer letters only.")])
    last_name_kh = StringField(validators=[Optional(), Length(max=15), Regexp(REGEX_KHMER, message="Please enter Khmer letters only.")])
    gender = RadioField('Gender',choices=[('M','Male'),('F','Female'),('O','Other')], default='F', validators=[DataRequired()])
    date_of_birth = StringField(validators=[DataRequired(), Length(max=10)])
    phone = StringField(validators=[DataRequired(), Length(min=9, max=10), Regexp(REGEX_PHONE, message="Please enter number only.")])
    email = StringField(validators=[Optional(), Length(max=50), Email()])
    address = StringField(validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Update')

    def validate_date_of_birth(self, date_of_birth):
        birth_date = datetime.strptime(date_of_birth.data, '%Y-%m-%d')
        age = int((datetime.today() - birth_date).days/365.2425)

        if age < 18:
            raise ValidationError('Age must be at least 18 years old.')

