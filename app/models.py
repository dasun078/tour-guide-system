from . import db
from datetime import datetime


class User(db.Model):
    """User model representing application users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    phone = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trips = db.relationship('Trip', backref='user', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', backref='user', lazy=True, cascade="all, delete-orphan")
    attractions = db.relationship('Attraction', backref='added_by_user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"


class Trip(db.Model):
    """Trip model for managing user-planned trips."""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    activities = db.Column(db.String(500), nullable=True)
    budget = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    feedbacks = db.relationship('Feedback', backref='trip', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trip to {self.destination} by User {self.user_id}>"


class Feedback(db.Model):
    """Feedback model to collect user feedback for trips."""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=True)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating from 1 to 5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback by User {self.user_id} for Trip {self.trip_id}>"


class Attraction(db.Model):
    """Attraction model for managing points of interest."""
    __tablename__ = 'attractions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Attraction {self.name} at {self.location}>"
