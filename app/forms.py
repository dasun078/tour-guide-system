from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, DateField, BooleanField, SelectField, SelectMultipleField
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
    arrival_date = DateField(
        'Arrival Date',
        validators=[DataRequired(message="Arrival date is required.")],
        format='%Y-%m-%d',
        description="Enter a date in the format YYYY-MM-DD."
    )
    departure_date = DateField(
        'Departure Date',
        validators=[DataRequired(message="Departure date is required.")],
        format='%Y-%m-%d',
        description="Enter a date in the format YYYY-MM-DD."
    )
    passport_number = StringField(
        'Passport Number',
        validators=[DataRequired(message="Passport number is required.")]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[DataRequired(message="Phone number is required.")]
    )
    number_of_people = FloatField(
        'Number of People',
        validators=[DataRequired(message="Number of people is required."), NumberRange(min=1, message="At least one person is required.")]
    )
    budget = FloatField(
        'Budget (USD)',
        validators=[
            DataRequired(message="Budget is required."),
            NumberRange(min=0, message="Budget must be a positive number.")
        ]
    )
    travel_modes = SelectMultipleField(
        'Travel Modes',
        choices=[('Car', 'Car'), ('Bus', 'Bus'), ('Train', 'Train'), ('Flight', 'Flight'), ('Boat', 'Boat')],
        validators=[Optional()],
        description="Select all applicable travel modes."
    )
    hotel = StringField(
        'Preferred Hotel',
        validators=[
            Optional(),
            Length(max=500, message="Hotel description must be 500 characters or less.")
        ]
    )
    destinations = TextAreaField(
        'Destinations',
        validators=[DataRequired(message="Please enter at least one destination.")]
    )
    activities = TextAreaField(
        'Activities for Each Destination',
        validators=[Optional(), Length(max=1000, message="Activities description must be 1000 characters or less.")]
    )
    submit = SubmitField('Plan Trip')

class FeedbackForm(FlaskForm):
    """Form for submitting feedback."""
    feedback_text = TextAreaField(
        'Feedback',
        validators=[
            DataRequired(message="Feedback is required."),
            Length(max=500, message="Feedback must be 500 characters or less.")
        ]
    )
    rating = SelectField(
        'Rating',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        validators=[DataRequired(message="Rating is required.")],
        coerce=int
    )
    submit = SubmitField('Submit Feedback')

class PaymentForm(FlaskForm):
    """Form for managing payments."""
    amount = FloatField(
        'Amount',
        validators=[
            DataRequired(message="Amount is required."),
            NumberRange(min=0, message="Amount must be a positive number.")
        ]
    )
    payment_status = SelectField(
        'Payment Status',
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        validators=[DataRequired(message="Payment status is required.")]
    )
    submit = SubmitField('Submit Payment')

class NotificationForm(FlaskForm):
    """Form for creating notifications."""
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Message is required."),
            Length(max=500, message="Message must be 500 characters or less.")
        ]
    )
    is_read = BooleanField('Mark as Read')
    submit = SubmitField('Send Notification')
