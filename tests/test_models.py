import unittest
from app import create_app, db
from app.models import User, Trip

class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up a test client and database."""
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add sample data
        self.user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down the database after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """Test creating a User model instance."""
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')

    def test_trip_creation(self):
        """Test creating a Trip model instance."""
        trip = Trip(
            user_id=self.user.id,
            destination='Colombo',
            activities='Beach, Cultural',
            budget=500.0
        )
        db.session.add(trip)
        db.session.commit()

        trip_from_db = Trip.query.filter_by(destination='Colombo').first()
        self.assertIsNotNone(trip_from_db)
        self.assertEqual(trip_from_db.destination, 'Colombo')
        self.assertEqual(trip_from_db.activities, 'Beach, Cultural')
        self.assertEqual(trip_from_db.budget, 500.0)
        self.assertEqual(trip_from_db.user_id, self.user.id)

    def test_user_relationship(self):
        """Test the relationship between User and Trip models."""
        trip = Trip(
            user_id=self.user.id,
            destination='Kandy',
            activities='Adventure, Wildlife',
            budget=300.0
        )
        db.session.add(trip)
        db.session.commit()

        user_from_db = User.query.get(self.user.id)
        self.assertEqual(len(user_from_db.trips), 1)
        self.assertEqual(user_from_db.trips[0].destination, 'Kandy')

if __name__ == '__main__':
    unittest.main()
