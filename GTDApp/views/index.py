from flask import request, render_template, redirect
from flask_login import login_user, login_required, logout_user, UserMixin, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from GTDApp import app, login_manager
from GTDApp.repo import UserRepo


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
    return LoggedInUserWrapper(UserRepo.get_user_by_id(user_id))


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    if current_user and current_user.is_authenticated:
        return redirect("/home")
    error = None
    if request.method == "POST":
        user = UserRepo.get_user_by_username(request.form["username"])
        if UserRepo.verify_user(request.form["username"], request.form["password"]):
            user = LoggedInUserWrapper(user)
            login_user(user)
            return redirect("/home")
        else:
            error = "Invalid Credentials. Please try again."
    return render_template("login.html", error=error)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user and current_user.is_authenticated:
        return redirect("/home")
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # TODO: Do an actual registration
        print(form.username.data, form.email.data,
                    form.password.data)
        flash('Thanks for registering')
        return redirect('/home')
    return render_template('register.html', form=form)


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
