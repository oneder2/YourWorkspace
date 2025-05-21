#!/bin/bash
# Script to fix API connection issues and run tests

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print header
print_header() {
    echo -e "\n${PURPLE}=========================================================================${NC}"
    echo -e "${PURPLE}${1}${NC}"
    echo -e "${PURPLE}=========================================================================${NC}\n"
}

# Print step
print_step() {
    echo -e "${BLUE}[STEP]${NC} ${1}"
}

# Print success
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} ${1}"
}

# Print error
print_error() {
    echo -e "${RED}[ERROR]${NC} ${1}"
}

# Print warning
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} ${1}"
}

# Print info
print_info() {
    echo -e "${CYAN}[INFO]${NC} ${1}"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main script
print_header "API Connection Fix Script"

# Check if Python is installed
if ! command_exists python; then
    print_error "Python is not installed. Please install Python 3.x and try again."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip; then
    print_error "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if the backend directory exists
if [ ! -d "backend" ]; then
    print_error "Backend directory not found. Please run this script from the project root directory."
    exit 1
fi

# Check if the frontend directory exists
if [ ! -d "svelte@latest" ]; then
    print_error "Frontend directory not found. Please run this script from the project root directory."
    exit 1
fi

# Install required Python packages
print_step "Installing required Python packages..."
pip install flask flask-cors flask-sqlalchemy flask-migrate flask-bcrypt flask-jwt-extended python-dotenv requests

# Initialize the SQLite database
print_step "Initializing the SQLite database..."
cd backend
python init_db.py
cd ..

# Run the API connection test
print_step "Running API connection test..."
python api_connection_test.py

# Ask if the user wants to start the servers
read -p "Do you want to start the backend and frontend servers? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Start the backend server
    print_step "Starting the backend server..."
    cd backend
    python run.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for the backend server to start
    print_info "Waiting for the backend server to start..."
    sleep 3
    
    # Start the frontend server
    print_step "Starting the frontend server..."
    cd svelte@latest
    if command_exists npm; then
        npm run dev &
        FRONTEND_PID=$!
    else
        print_error "npm is not installed. Please install Node.js and npm, then run 'npm run dev' in the svelte@latest directory."
    fi
    cd ..
    
    # Wait for the frontend server to start
    print_info "Waiting for the frontend server to start..."
    sleep 5
    
    # Run the API endpoint test
    print_step "Running API endpoint test..."
    python test_api_endpoints.py
    
    # Print success message
    print_success "API connection fix applied and tested successfully!"
    print_info "Backend server is running with PID $BACKEND_PID"
    if [ -n "$FRONTEND_PID" ]; then
        print_info "Frontend server is running with PID $FRONTEND_PID"
    fi
    
    # Keep the servers running until the user presses Ctrl+C
    print_info "Press Ctrl+C to stop the servers and exit..."
    trap "kill $BACKEND_PID 2>/dev/null; if [ -n \"$FRONTEND_PID\" ]; then kill $FRONTEND_PID 2>/dev/null; fi; echo -e \"\n${GREEN}Servers stopped.${NC}\"" EXIT
    wait
else
    print_info "You can start the servers manually:"
    print_info "1. Start the backend server: cd backend && python run.py"
    print_info "2. Start the frontend server: cd svelte@latest && npm run dev"
    print_info "3. Run the API endpoint test: python test_api_endpoints.py"
fi
