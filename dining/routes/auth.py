"""
diningapp auth () routes.
URLs include:
/login/
/resetpassword/
/register/
/logout/
"""
from flask import session, redirect, url_for, request, flash, render_template
from requests import HTTPError
from dining import app, firebase_auth, firebase_db
from dining.forms import (LoginForm, RegisterForm, ResetPasswordForm)
from dining.utils import (
    login_required, redirect_dest, get_redirect_url, refresh_user_token, ERROR_MESSAGE_DICT)

@app.route('/login/', methods=["GET", "POST"])
def login():
    """Display the login page."""
    # Check if the user is logged in by (1) checking to see if there are login tokens available
    # and (2) refreshing the user's token to see if the token is valid. 
    # See dining/utils.py for more on what refresh_user_token() does.
    if 'token' in session and 'user_id' in session and refresh_user_token():
        flash("Already logged in!", "warning")
        return redirect(url_for('index'))

    register_url = url_for("register")
    if "next" in request.args:
        register_url = get_redirect_url('register', request.args, False)

    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                email = form.email.data
                password = form.password.data

                # TODO(SESSION1) FILL THIS LINE IN: Call the Firebase auth service to get the user credentials.
                user = firebase_auth.sign_in_with_email_and_password(email, password)

                # TODO(SESSION2) Replace this line with a call to the Firebase database service to get the user from the users table.
                user_resp = {}


                user_favorites = user_resp.get("favorites", {})

                # setting session variables
                session["token"] = user["idToken"]
                session["refresh_token"] = user["refreshToken"]
                # same as the one on Firebase
                session["user_id"] = user["localId"]

                flash("Successfully logged in!", "success")
                return redirect_dest(url_for('index'), request.args)
            except HTTPError:
                flash("Try again (invalid email or password)", "warning")
                return render_template('login.html', login_form=form, register_url=register_url, pagetitle="Dining App | Login")
    return render_template('login.html', login_form=form, register_url=register_url, pagetitle="Dining App | Login" )


@app.route('/resetpassword/', methods=["GET", "POST"])
def resetpassword():
    """Display the forgot password page."""
    form = ResetPasswordForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                # TODO(SESSION1): Write a line here to reset the user's password given their email address.
                # Then clear the session's information, and it will redirect to the login page
                # for the user to log in again.
                email = form.email.data
                firebase_auth.send_password_reset_email(email)
                flash(("Email sent successfully - check your inbox to "
                       "reset your password."),
                      "success")
                return redirect(url_for('login'))
            except HTTPError:
                flash("Something went wrong. Try again", "warning")
                return render_template("reset_password.html", form=form, pagetitle="Dining App | Reset Password")
    return render_template('reset_password.html', form=form, pagetitle="Dining App | Reset Password")

@app.route('/register/', methods=["GET", "POST"])
def register():
    """Display the user registration page."""
    form = RegisterForm(request.form)
    new_user = None
    if request.method == "POST":
        if form.validate():
            try:
                name = form.name.data
                email = form.email.data
                password = form.password.data

                # (1) Create the user in the authentication database.
                # TODO(SESSION1) Replace None here with a call to Firebase: Create a user in the Firebase auth service.
                new_user = firebase_auth.create_user_with_email_and_password(email, password)  # Modify this line

                # (2) Create the user in the users database.
                user_data = {
                    "name": name,
                    "favorites": []
                }

                # (3) Push that new user to the Firebase db, the users table.
                # TODO(SESSION2): Write a line below to push the new user object to Firebase.


                
                # (4) Set initial session values
                session["token"] = new_user.get("idToken", "")
                # same as the one on Firebase
                session["user_id"] = new_user.get("localId", "")
                session["refresh_token"] = new_user.get("refreshToken", "")

                return redirect_dest(url_for('index'), request.args)

            except HTTPError as err:
                if err.response and \
                   err.response.get("error", {}).get("message") in ERROR_MESSAGE_DICT:
                    flash("Registration failed - " +
                          ERROR_MESSAGE_DICT[err.response["error"]["message"]], "warning")
                else:
                    flash("Registration failed - unknown error", "warning")
                return render_template('register.html', register_form=form, pagetitle="Dining App | Register")
    return render_template('register.html', register_form=form, pagetitle="Dining App | Register")


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    """Display the logout page."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))