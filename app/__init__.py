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
        app.logger.info("Database initialized successfully.")
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully.")
        except Exception as e:
            app.logger.error(f"Error creating database tables: {str(e)}")

    return app