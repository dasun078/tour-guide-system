from app import create_app

# Create the Flask app instance using the factory function
app = create_app()

# Run the application
if __name__ == "__main__":
    # Ensure the app runs in debug mode for development
    app.run(host="127.0.0.1", port=5000, debug=True)
