from app import create_app
import os

# Determine the environment and load the appropriate configuration
environment = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set

# Create the Flask app instance using the factory function
app = create_app(f'config.{environment.capitalize()}Config')

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="127.0.0.1", port=5000, debug=app.config['DEBUG'])
