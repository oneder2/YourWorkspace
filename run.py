# /your_project_root/run.py
# This script imports the app factory and runs the Flask development server.

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Make sure to create a .env file in your project root
# Place .env in the same directory as this run.py file
load_dotenv()

# Import the app factory function from our app package
from app import create_app

# Create the Flask app instance using the factory
# Pass the appropriate configuration name (e.g., 'development', 'production')
# Get the configuration name from the FLASK_CONFIG environment variable
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Run the app using Flask's built-in development server
    # host='0.0.0.0' makes it accessible on your local network
    # debug=True enables debugger and auto-reloader (reads DEBUG from config)
    # port can be set via PORT env var or defaults to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))

