from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config_name or 'config.DevelopmentConfig')  

    # Initialize extensions
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        print("Database initialized successfully.")
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")

    # Register your blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
