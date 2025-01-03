from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Name is required."),
            Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Password confirmation is required."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required.")
        ]
    )
    submit = SubmitField('Login')


class TripForm(FlaskForm):
    """Form for planning a trip."""
    destination = StringField(
        'Destination',
        validators=[
            DataRequired(message="Destination is required."),
            Length(min=2, max=100, message="Destination must be between 2 and 100 characters.")
        ]
    )
    activities = TextAreaField(
        'Activities',
        validators=[
            Optional(),
            Length(max=500, message="Activities description must be 500 characters or less.")
        ]
    )
    budget = FloatField(
        'Budget',
        validators=[
            Optional(),
            NumberRange(min=0, message="Budget must be a positive number.")
        ]
    )
    date = DateField(
        'Date',
        validators=[
            Optional()
        ],
        format='%Y-%m-%d',
        description="Enter a date in the format YYYY-MM-DD."
    )
    submit = SubmitField('Plan Trip')
