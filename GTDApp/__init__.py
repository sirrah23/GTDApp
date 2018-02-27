from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
from GTDApp.repo import GTDRepo


app = Flask(__name__)
app.secret_key = "myspookysecret"


login_manager = LoginManager()
login_manager.init_app(app)


GTDRepo.connect("gtd") # TODO: config


class LoggedInUserWrapper(UserMixin):

    def __init__(self, u):
        self.u = u

    def get_id(self):
        if not self.u:
            return None
        return str(self.u.id)

    def get_obj_id(self):
        if not self.u:
            return None
        return self.u.id


@login_manager.user_loader
def load_user(user_id):
    return LoggedInUserWrapper(GTDRepo.get_user_by_id(user_id))


# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = GTDRepo.get_user_by_username(request.form["username"])
        if user and user.password == request.form["password"]:
            user = LoggedInUserWrapper(user)
            login_user(user)
            return redirect("/home")
        else:
            error = "Invalid Credentials. Please try again."
    return render_template("login.html", error=error)


from GTDApp.views import index
from GTDApp.views import task
from GTDApp.views import item
