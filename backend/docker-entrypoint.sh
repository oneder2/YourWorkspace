#!/bin/bash
set -e

# Function to wait for database to be ready
wait_for_db() {
    echo "Checking if database is ready..."
    
    # Create instance directory if it doesn't exist
    mkdir -p instance
    
    # Check if we can connect to the database
    python -c "
import sqlite3
try:
    conn = sqlite3.connect('instance/prod.sqlite')
    conn.close()
    print('Database is ready')
except Exception as e:
    print(f'Database is not ready: {e}')
    exit(1)
"
}

# Initialize the database if it doesn't exist
init_db() {
    echo "Initializing database..."
    
    # Check if the database file exists
    if [ ! -f "instance/prod.sqlite" ]; then
        echo "Database file does not exist. Creating..."
        python init_db.py
    else
        echo "Database file already exists."
    fi
}

# Run database migrations
run_migrations() {
    echo "Running database migrations..."
    flask db upgrade
}

# Main function
main() {
    # Wait for the database to be ready
    wait_for_db
    
    # Initialize the database if needed
    init_db
    
    # Run database migrations
    run_migrations
    
    # Start the application
    exec "$@"
}

# Run the main function with the provided arguments
main "$@"
