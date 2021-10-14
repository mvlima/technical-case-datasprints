## Turns website folder into a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Initialize database
db = SQLAlchemy() # Object
DB_NAME = "database.db" # Name
app = Flask(__name__)

def create_app():

    app.config['SECRET_KEY'] = 'thisisthesecretkeylol'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Where the database is located
    db.init_app(app) # Initializa database

    # Import Blueprint
    from .views import views
    from .auth import auth

    # Register Blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Initialize models.py file and define the User model before creating the database
    from .models import User

    create_database(app)
    
    # If the user is not logged in and login is required, where should flask redirect them
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    # What user we're looking for
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Check if the database already exists, if not, create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")