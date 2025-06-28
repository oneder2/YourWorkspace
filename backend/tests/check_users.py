from app import create_app
from app.models.user import User
from app.extensions import db

app = create_app()

with app.app_context():
    users = User.query.all()
    print('Users in database:')
    for user in users:
        print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}')
