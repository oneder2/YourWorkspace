#!/usr/bin/env python3
"""
Database Initialization Script
This script initializes the SQLite database for the Flask backend.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the app factory function
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.todo_item import TodoItem
from app.models.achievement import Achievement
from app.models.future_plan import FuturePlan

def init_db():
    """Initialize the database."""
    print("Initializing database...")
    
    # Create the Flask app instance
    app = create_app('development')
    
    # Ensure the instance directory exists
    instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created instance directory: {instance_dir}")
    
    # Create the database tables
    with app.app_context():
        db.create_all()
        print("Database tables created.")
        
        # Check if a test user already exists
        test_user = User.query.filter_by(email="test@example.com").first()
        if not test_user:
            # Create a test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                password="password123"
            )
            db.session.add(test_user)
            db.session.commit()
            print("Test user created.")
        else:
            print("Test user already exists.")
        
        # Create some sample data
        create_sample_data(test_user.id)
        
        print("Database initialization complete.")

def create_sample_data(user_id):
    """Create sample data for the test user."""
    # Create sample todo items
    todo_count = TodoItem.query.filter_by(user_id=user_id).count()
    if todo_count == 0:
        todos = [
            TodoItem(
                user_id=user_id,
                title="Complete project setup",
                description="Set up the development environment and initialize the project.",
                status="completed",
                priority="high",
                is_current_focus=False
            ),
            TodoItem(
                user_id=user_id,
                title="Implement user authentication",
                description="Add user registration, login, and authentication functionality.",
                status="in_progress",
                priority="high",
                is_current_focus=True
            ),
            TodoItem(
                user_id=user_id,
                title="Design database schema",
                description="Create the database schema for the application.",
                status="pending",
                priority="medium",
                is_current_focus=False
            )
        ]
        
        db.session.add_all(todos)
        db.session.commit()
        print(f"Created {len(todos)} sample todo items.")
    else:
        print(f"Sample todo items already exist ({todo_count} items).")
    
    # Create sample achievements
    achievement_count = Achievement.query.filter_by(user_id=user_id).count()
    if achievement_count == 0:
        achievements = [
            Achievement(
                user_id=user_id,
                title="Completed Frontend Development Course",
                description="Finished a comprehensive course on modern frontend development.",
                date_achieved="2023-01-15"
            ),
            Achievement(
                user_id=user_id,
                title="Launched First Web Application",
                description="Successfully deployed my first web application to production.",
                date_achieved="2023-03-20"
            )
        ]
        
        db.session.add_all(achievements)
        db.session.commit()
        print(f"Created {len(achievements)} sample achievements.")
    else:
        print(f"Sample achievements already exist ({achievement_count} items).")
    
    # Create sample future plans
    plan_count = FuturePlan.query.filter_by(user_id=user_id).count()
    if plan_count == 0:
        plans = [
            FuturePlan(
                user_id=user_id,
                title="Learn Machine Learning",
                description="Complete a course on machine learning fundamentals.",
                goal_type="learning",
                target_date="2023-12-31",
                status="active"
            ),
            FuturePlan(
                user_id=user_id,
                title="Build a Mobile App",
                description="Develop and publish a mobile application.",
                goal_type="project",
                target_date="2024-06-30",
                status="active"
            )
        ]
        
        db.session.add_all(plans)
        db.session.commit()
        print(f"Created {len(plans)} sample future plans.")
    else:
        print(f"Sample future plans already exist ({plan_count} items).")

if __name__ == "__main__":
    init_db()
