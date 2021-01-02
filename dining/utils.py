"""
dining app utils.
This utility functions for the flask app.
"""
import math
import uuid
from functools import wraps
from re import compile, sub
from urllib.parse import urlparse, urljoin
import requests as rq
from requests import HTTPError
from flask import session, flash, redirect, url_for, jsonify, abort, request
from dining import firebase_auth, firebase_db

ERROR_MESSAGE_DICT = {
    "WEAK_PASSWORD : Password should be at least 6 characters":
    "password should be at least 6 characters.",
    "EMAIL_EXISTS": "account already exists under provided email address."}

## AUTH HELPERS
def refresh_user_token():
    """ 
    Refresh expired tokens. 
    This helps the user stay logged in and makes sure only valid users are logging in. 
    """
    # If the refresh token doesn't exist, then log the current user out because something isn't right.
    if 'refresh_token' not in session:
        # should always be checking anyways whether a user is logged in, but check here too anyways
        session.clear()
        return False
    try:
        # TODO(SESSION1): Write a line to refresh the user's token using the refresh token stored in the session.
        # Then write another line to store the new token and refresh token in the session.
        #
        #
        return True  # keep this

    # A few problems can occur during refreshing a user token. For instance, that token might not belong to any user in our system.
    # In that case, an "HTTPError" will be thrown, and this except block will catch that.
    # If the error is something we know might happen, like a user isn't found in our db, or the token is invalid, then we just log out the user
    # and have them log in again.

    # If it's something else, then idk what happened lol, so just abort(404), which redirects the user to a 404 :( page.
    except HTTPError as err:
        if (err.response and err.response.get("error", {}).get("message") in
                ["USER_NOT_FOUND", "INVALID_REFRESH_TOKEN"]):
            session.clear()
            return False
        abort(404)

def get_redirect_url(fallback, args={}, go_to_dest=True):
    """ Generate the redirect URL if able to, otherwise generate fallback/ """
    # go_to_dest refers to whether you want to try to redirect to the next param
    # or just hold it for redirecting to fallback
    dest = request.args.get('next')
    redirect_args = {k: v for k, v in args.items() if k != "next"}
    try:
        dest_url = url_for(dest, **redirect_args) if go_to_dest else url_for(fallback, **args)
        if not is_safe_url(dest_url):
            return fallback
    except:
        return fallback
    return dest_url

def redirect_dest(fallback, args={}):
    """redirect URL function"""
    url = get_redirect_url(fallback, args, True)
    return redirect(url)

################### FUNCTION DECORATORS ######################


def login_required(func):
    """Decorator for login required routes."""
    @wraps(func)
    def wrap(*args, **kwargs):
        # TODO(SESSION1): Write a line to validate a token (check to see if it exists and make sure it's a real token)
        if 'token' in session and 'user_id' in session:
            return func(*args, **kwargs)
        # else
        flash("Login required", "warning")
        return redirect(url_for('login'))
    return wrap