from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Trip
from .forms import RegistrationForm, LoginForm, TripForm

main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/')
def home():
    return render_template('index.html')

# Travel News route
@main_bp.route('/travel_news')
def travel_news():
    return render_template('travel_news.html')

# Seasonal Favorites route
@main_bp.route('/seasonal_favorites')
def seasonal_favorites():
    return render_template('seasonal_favorites.html')

# New Attractions route
@main_bp.route('/new_attractions')
def new_attractions():
    return render_template('new_attractions.html')

# User registration route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            user = User(name=form.name.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: Unable to register. Email might already be in use.', 'danger')
    return render_template('register.html', form=form)

# User login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# User dashboard route
@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in.', 'warning')
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    trips = Trip.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, trips=trips)

# Plan a trip route
@main_bp.route('/plan_trip', methods=['GET', 'POST'])
def plan_trip():
    if 'user_id' not in session:
        flash('Please log in to plan a trip.', 'warning')
        return redirect(url_for('main.login'))
    
    form = TripForm()
    if form.validate_on_submit():
        try:
            trip = Trip(
                user_id=session['user_id'],
                destination=form.destination.data,
                activities=form.activities.data,
                budget=form.budget.data,
                date=form.date.data
            )
            db.session.add(trip)
            db.session.commit()
            flash('Trip planned successfully!', 'success')
            return redirect(url_for('main.map', destination=form.destination.data))
        except Exception as e:
            db.session.rollback()
            flash('Error: Unable to save the trip. Please try again.', 'danger')
    return render_template('plan_trip.html', form=form)

# Map route (used after planning a trip)
@main_bp.route('/map/<destination>')
def map(destination):
    return render_template('map.html', destination=destination)

# Logout route
@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.home'))
