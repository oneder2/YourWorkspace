#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${2}${1}${NC}"
}

# Function to print success messages
print_success() {
    print_message "$1" "${GREEN}"
}

# Function to print warning messages
print_warning() {
    print_message "$1" "${YELLOW}"
}

# Function to print error messages
print_error() {
    print_message "$1" "${RED}"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker and try again."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating one with default values..."
        echo "SECRET_KEY=default_secret_key_change_in_production" > .env
        echo "JWT_SECRET_KEY=default_jwt_secret_key_change_in_production" >> .env
        print_warning "Please update the .env file with your own values before deploying to production."
    fi
}

# Function to build and start the containers
start_containers() {
    print_success "Building and starting containers..."
    docker-compose up --build -d
}

# Function to stop the containers
stop_containers() {
    print_success "Stopping containers..."
    docker-compose down
}

# Function to show container logs
show_logs() {
    print_success "Showing container logs..."
    docker-compose logs -f
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo "Options:"
    echo "  start    Build and start the containers"
    echo "  stop     Stop the containers"
    echo "  restart  Restart the containers"
    echo "  logs     Show container logs"
    echo "  help     Show this help message"
}

# Main function
main() {
    check_docker
    check_env_file

    case "$1" in
        start)
            start_containers
            ;;
        stop)
            stop_containers
            ;;
        restart)
            stop_containers
            start_containers
            ;;
        logs)
            show_logs
            ;;
        help)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

# Run the main function with the provided arguments
main "$@"
