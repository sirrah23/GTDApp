from flask import Flask, render_template, redirect, request, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)

# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect("/home")
    return render_template("login.html", error=error)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.username.data, form.email.data,
                    form.password.data)
        flash('Thanks for registering')
        return redirect('/home')
    return render_template('register.html', form=form)
