import os
from flask import Flask
from flask_login import LoginManager
from GTDApp.repo import GTDRepo, ItemRepo


# Initialize the app
app = Flask(__name__)
app.secret_key = "myspookysecret"

if os.environ.get("CONFIG_TYPE") == "test":
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "..", "./config/config.cfg.test"))
else:
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "..", "./config/config.cfg.default"))


# Initialize the login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)


# Connect to the database
GTDRepo.connect(app.config["DBNAME"])
ItemRepo.connect(app.config["DBNAME"])


from GTDApp.views import index
from GTDApp.views import item
from GTDApp.views import task
from GTDApp.views import project
