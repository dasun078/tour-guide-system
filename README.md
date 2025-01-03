# Tour Guide System

## Overview
The **Tour Guide System** is a web application designed to help users plan personalized trips in Sri Lanka. The platform allows users to register, log in, and create itineraries tailored to their preferences, including destinations, activities, and budgets. It also integrates with Google Maps for location-based features.

## Features
- User registration and authentication
- Dynamic trip planning
- Google Maps integration for location and navigation
- Responsive design for mobile and desktop
- Secure data handling with encrypted credentials

## Tech Stack
- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Migrate
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **Database**: MySQL (via PyMySQL)
- **APIs**: Google Maps API

## Setup Instructions

### Prerequisites
1. Install Python 3.8 or later.
2. Install MySQL and create a database for the project.
3. Obtain a Google Maps API key.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/tour-guide-system.git
   cd tour-guide-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables in a `.env` file:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

7. Open the application in your browser at `http://127.0.0.1:5000`.

## Testing
Run unit tests to verify functionality:
```bash
python -m unittest discover -s tests
```

## File Structure
```
TourGuideSystem/
│
├── app/                  # Application source code
│   ├── __init__.py       # App initialization
│   ├── routes.py         # Application routes
│   ├── models.py         # Database models
│   ├── forms.py          # Forms for input validation
│   └── static/           # Static assets (CSS, JS, images)
│
├── templates/            # HTML templates
├── migrations/           # Database migrations
├── tests/                # Unit tests
├── .env                  # Environment variables
├── .gitignore            # Ignored files
├── config.py             # Configuration file
├── requirements.txt      # Python dependencies
├── run.py                # Entry point for the application
└── README.md             # Project overview and instructions
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request.

## Contact
For questions or suggestions, please contact the developer at [email@example.com].
