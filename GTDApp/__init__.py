from flask import Flask
from flask_login import LoginManager
from GTDApp.repo import GTDRepo


# Initialize the app
app = Flask(__name__)
app.secret_key = "myspookysecret"


# Initialize the login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)


# Connect to the database
GTDRepo.connect("gtd") # TODO: config


from GTDApp.views import index
from GTDApp.views import task
from GTDApp.views import item
