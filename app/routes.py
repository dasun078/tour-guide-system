from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Trip, Destination, UserPreference
from app.forms import RegistrationForm, LoginForm, TripForm
import logging

# Setup logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

# Helper function to get the current logged-in user
def current_user():
    if 'user_id' in session:
        user_id = session['user_id']
        logger.debug(f"Fetching current user with ID: {user_id}")
        return User.query.get(user_id)
    logger.debug("No user logged in.")
    return None

@main_bp.route('/')
def home():
    """Render the home page."""
    logger.debug("Rendering the home page.")
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            logger.info(f"User registered: {form.email.data}")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {e}", 'danger')
            logger.error(f"Error during registration: {e}")
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Admin login
        if form.email.data == 'dasungunarathned15@gmail.com' and form.password.data == 'DASUN@123':
            admin_user = User.query.filter_by(email='dasungunarathned15@gmail.com').first()
            if not admin_user:
                admin_user = User(
                    name='Admin',
                    email='dasungunarathned15@gmail.com',
                    password=generate_password_hash('DASUN@123', method='pbkdf2:sha256'),
                    is_admin=True
                )
                db.session.add(admin_user)
                db.session.commit()
            session['user_id'] = admin_user.id
            session['is_admin'] = admin_user.is_admin
            flash('Admin login successful!', 'success')
            logger.info("Admin logged in.")
            return redirect(url_for('main.dashboard'))

        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            logger.info(f"User logged in: {user.email}")
            return redirect(url_for('main.dashboard'))

        flash('Invalid email or password.', 'danger')
        logger.warning(f"Failed login attempt for email: {form.email.data}")
    return render_template('login.html', form=form)

@main_bp.route('/dashboard')
def dashboard():
    """User dashboard."""
    user = current_user()
    if not user:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('main.login'))

    trips = Trip.query.filter_by(user_id=user.id).all()
    preferences = [pref.preference for pref in user.preferences]
    logger.debug(f"User {user.id} trips: {trips}")
    logger.debug(f"User {user.id} preferences: {preferences}")

    return render_template(
        'dashboard.html',
        user=user,
        trips=trips,
        preferences=preferences
    )

@main_bp.route('/plan_trip', methods=['GET', 'POST'])
def plan_trip():
    """Plan a trip with detailed user inputs and travel modes."""
    user = current_user()
    if not user:
        flash('Please log in to plan a trip.', 'warning')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        try:
            arrival_date = request.form.get('arrival_date')
            departure_date = request.form.get('departure_date')
            passport_number = request.form.get('passport_number')
            phone_number = request.form.get('phone_number')
            number_of_people = request.form.get('number_of_people')
            destinations = request.form.getlist('destinations[]')
            activities = request.form.getlist('activities[]')
            travel_modes = request.form.getlist('travel_modes[]')
            budget = request.form.get('budget')
            hotel = request.form.get('hotel')

            if not (arrival_date and departure_date and passport_number and phone_number and destinations and budget and hotel):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('main.plan_trip'))

            trip = Trip(
                user_id=user.id,
                arrival_date=arrival_date,
                departure_date=departure_date,
                passport_number=passport_number,
                phone_number=phone_number,
                number_of_people=int(number_of_people),
                hotel=hotel,
                budget=float(budget)
            )
            db.session.add(trip)
            db.session.flush()

            for destination, activity, travel_mode in zip(destinations, activities, travel_modes):
                destination_entry = Destination(
                    trip_id=trip.id,
                    destination_name=destination,
                    activities=activity,
                    travel_mode=travel_mode
                )
                db.session.add(destination_entry)

            db.session.commit()
            flash('Trip planned successfully!', 'success')
            logger.info(f"Trip planned by user {user.id}: {trip}")
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error planning trip: {e}")
            flash('An error occurred while planning your trip. Please try again.', 'danger')

    hotel_suggestions = ["Hotel Colombo", "Kandy Hills Resort", "Sigiriya Haven", "Ella Green View"]

    return render_template('plan_trip.html', user=user, hotel_suggestions=hotel_suggestions)

@main_bp.route('/logout')
def logout():
    """User logout."""
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'info')
    logger.info("User logged out.")
    return redirect(url_for('main.home'))

@main_bp.route('/payments', methods=['GET', 'POST'])
def payments():
    """Render the payments page and handle payment submissions."""
    user = current_user()
    if not user:
        flash('Please log in to manage payments.', 'warning')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        try:
            payment_method = request.form.get('payment_method')
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')
            amount = float(request.form.get('amount', 0.0))

            if not all([payment_method, card_number, expiry_date, cvv, amount]):
                flash('All fields are required for payment.', 'danger')
                return redirect(url_for('main.payments'))

            flash('Payment processed successfully!', 'success')
            logger.info(f"Payment processed for user {user.id} using {payment_method}.")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            logger.error(f"Payment processing error: {e}")
            flash('Error processing payment. Please try again.', 'danger')

    return render_template('payments.html', user=user)

@main_bp.route('/save_preferences', methods=['POST'])
def save_preferences():
    """Save user preferences."""
    user = current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    preference = request.form.get('preference')
    if preference:
        new_pref = UserPreference(user_id=user.id, preference=preference)
        db.session.add(new_pref)
        db.session.commit()
        logger.info(f"Saved preference: {preference} for user {user.id}")
        return jsonify({'message': 'Preference saved successfully'}), 200

    logger.warning("Preference not provided in the request.")
    return jsonify({'error': 'Preference is required'}), 400

@main_bp.route('/recommend_destinations', methods=['GET'])
def recommend_destinations():
    """AI-powered destination recommendations."""
    user = current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    budget = request.args.get('budget', type=float)
    activities = request.args.get('activities', '').split(',')

    # Mock recommendation logic
    recommendations = [
        "Colombo", "Kandy", "Sigiriya", "Ella", "Galle"
    ]

    # Filter based on mock logic (replace with actual ML logic)
    filtered_recommendations = [
        dest for dest in recommendations if dest.lower().startswith('c') or dest.lower().startswith('e')
    ]

    logger.debug(f"Recommended destinations for user {user.id}: {filtered_recommendations}")
    return jsonify(filtered_recommendations), 200

@main_bp.route('/travel_news')
def travel_news():
    """Render the travel news page."""
    logger.debug("Rendering travel news page.")
    return render_template('travel_news.html')

@main_bp.route('/seasonal_favorites')
def seasonal_favorites():
    """Render the seasonal favorites page."""
    logger.debug("Rendering seasonal favorites page.")
    return render_template('seasonal_favorites.html')

@main_bp.route('/new_attractions')
def new_attractions():
    """Render the new attractions page."""
    logger.debug("Rendering new attractions page.")
    return render_template('new_attractions.html')
