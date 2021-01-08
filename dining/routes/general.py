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

    ## END CODE
    return render_template('index.html', user=user)
