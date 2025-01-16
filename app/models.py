from . import db
from datetime import datetime


class User(db.Model):
    """User model representing application users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trips = db.relationship('Trip', backref='user', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', backref='user', lazy=True, cascade="all, delete-orphan")
    preferences = db.relationship('UserPreference', backref='user', lazy=True, cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='user', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"


class Trip(db.Model):
    """Trip model for managing user-planned trips."""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    destinations = db.relationship('Destination', backref='trip', lazy=True, cascade="all, delete-orphan")
    hotel = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Trip by User {self.user_id} with budget {self.budget}>"


class Destination(db.Model):
    """Model to store destinations, activities, and travel modes for trips."""
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    destination_name = db.Column(db.String(100), nullable=False)
    activities = db.Column(db.Text, nullable=False)
    travel_mode = db.Column(db.String(50), nullable=False)  # New column for travel mode

    def __repr__(self):
        return f"<Destination {self.destination_name} for Trip {self.trip_id}>"


class Feedback(db.Model):
    """Feedback model to collect user feedback for trips."""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=True)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback by User {self.user_id} for Trip {self.trip_id}>"


class UserPreference(db.Model):
    """Model to store user preferences for generating personalized tour plans."""
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preference = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<UserPreference {self.preference} for User {self.user_id}>"


class TourPlan(db.Model):
    """Model for storing generated tour plans."""
    __tablename__ = 'tour_plans'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    pinpoints = db.Column(db.Text, nullable=True)
    payment_status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<TourPlan for Trip {self.trip_id}>"


class Payment(db.Model):
    """Model to track payments for trips."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.Enum('Pending', 'Completed', 'Failed'), default='Pending', nullable=False)

    def __repr__(self):
        return f"<Payment {self.amount} for Trip {self.trip_id} by User {self.user_id}>"


class Notification(db.Model):
    """Model to store user notifications."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification for User {self.user_id}: {self.message[:20]}...>"
