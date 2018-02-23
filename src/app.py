import json
from flask import Flask, render_template, redirect, request, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
from src.repo import GTDRepo


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


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.username.data, form.email.data,
                    form.password.data)
        flash('Thanks for registering')
        return redirect('/home')
    return render_template('register.html', form=form)

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/api/item", methods=["POST"])
@login_required
def item_add():
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        res = GTDRepo.add_item(payload["description"], uid)
        res["id"] = str(res["id"])
        res["success"] = True
    return json.dumps(res)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
