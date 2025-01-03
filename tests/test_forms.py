import unittest
from app.forms import RegistrationForm, LoginForm, TripForm

class TestForms(unittest.TestCase):
    def test_registration_form_valid_data(self):
        """Test registration form with valid data."""
        form = RegistrationForm(
            name="Test User",
            email="test@example.com",
            password="password123",
            confirm_password="password123"
        )
        self.assertTrue(form.validate())

    def test_registration_form_invalid_email(self):
        """Test registration form with an invalid email."""
        form = RegistrationForm(
            name="Test User",
            email="invalid-email",
            password="password123",
            confirm_password="password123"
        )
        self.assertFalse(form.validate())

    def test_registration_form_password_mismatch(self):
        """Test registration form with mismatched passwords."""
        form = RegistrationForm(
            name="Test User",
            email="test@example.com",
            password="password123",
            confirm_password="password456"
        )
        self.assertFalse(form.validate())

    def test_login_form_valid_data(self):
        """Test login form with valid data."""
        form = LoginForm(
            email="test@example.com",
            password="password123"
        )
        self.assertTrue(form.validate())

    def test_login_form_missing_data(self):
        """Test login form with missing data."""
        form = LoginForm(email="")
        self.assertFalse(form.validate())

    def test_trip_form_valid_data(self):
        """Test trip form with valid data."""
        form = TripForm(
            destination="Colombo",
            activities=["adventure", "beach"],
            budget=500
        )
        self.assertTrue(form.validate())

    def test_trip_form_missing_destination(self):
        """Test trip form with missing destination."""
        form = TripForm(
            destination="",
            activities=["adventure", "beach"],
            budget=500
        )
        self.assertFalse(form.validate())

    def test_trip_form_negative_budget(self):
        """Test trip form with a negative budget."""
        form = TripForm(
            destination="Colombo",
            activities=["adventure", "beach"],
            budget=-100
        )
        self.assertFalse(form.validate())
        
    def test_registration_form_valid_data(self):
        """Test registration form with valid data."""
        with self.app.app_context():  # Add this line
            form = RegistrationForm(
                name="Test User",
                email="test@example.com",
                password="password123",
                confirm_password="password123"
            )
            self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
