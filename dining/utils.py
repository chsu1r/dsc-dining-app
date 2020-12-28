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

ERROR_MESSAGE_DICT = {
    "WEAK_PASSWORD : Password should be at least 6 characters":
    "password should be at least 6 characters.",
    "EMAIL_EXISTS": "account already exists under provided email address."}

## AUTH HELPERS
def refresh_user_token():
    """Refresh expired tokens."""
    if 'refresh_token' not in session:
        # should always be checking anyways whether a user is logged in, but check here too anyways
        session.clear()
        return False
    try:
        # TODO(): FILL THIS IN: refresh the user's token using the refresh token stored in the session.
        # Then store the new token and refresh token in the session.
        return True
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
        # TODO: Validate Token (check to see if it exists and make sure it's a real token)
        if 'token' in session and 'user_id' in session:
            return func(*args, **kwargs)
        # else
        flash("Login required", "warning")
        return redirect(url_for('login'))
    return wrap