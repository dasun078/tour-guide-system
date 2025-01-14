from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the FLASK_ENV from environment variables
environment = os.getenv('FLASK_ENV', 'development')

# Create the Flask app instance using the factory function
app = create_app(f'config.{environment.capitalize()}Config')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config['DEBUG'])