"""
dining app general () routes.
URLs include:
/
/aboutus/
/faq/
/terms/
/privacy/
/stop/
"""
from flask import render_template, flash, request, redirect, session
from dining import app, firebase_db
from dining.utils import refresh_user_token
from requests import HTTPError

@app.route('/')
def index():
    """Display index (home) route."""
    user = None
    # TODO(SESSION2): Check to see if the user is logged in, and if so, then fetch user information from Firebase database.
    ## CODE HERE
    if 'token' in session and 'user_id' in session and refresh_user_token():  # if logged in
        try:
            users_db = firebase_db.child('users')
            user = users_db.child(session['user_id']).get(session['token']).val()

        except HTTPError as err:
            print("There was an error in getting the user information from Firebase.")
            raise err
    ## END CODE HERE
    return render_template('index.html', user=user)
