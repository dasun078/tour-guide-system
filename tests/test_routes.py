import unittest
from app import create_app, db
from app.models import User

class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up a test client and database."""
        self.app = create_app('testing')  # Ensure 'testing' is defined in config.py
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Create a sample user
        user = User(name='Test User', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Tear down the database after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        """Test the home page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Tour Guide System', response.data)

    def test_register_route(self):
        """Test the user registration route."""
        response = self.client.post('/register', data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            self.assertIsNotNone(user)

    def test_login_route(self):
        """Test the user login route."""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_dashboard_route_without_login(self):
        """Test the dashboard route without login."""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dashboard_route_with_login(self):
        """Test the dashboard route after login."""
        with self.client:
            self.client.post('/login', data={
                'email': 'test@example.com',
                'password': 'password'
            })
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to Your Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()
