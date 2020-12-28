"""
dining app error () routes.
Handles 403, 404 and 500 errors.
"""
from flask import render_template, flash
from dining import app

@app.errorhandler(404)
def page_not_found(error):
    """Abort 404 error page."""
    return render_template('error.html', error_msg="404 Page Not Found", pagetitle="404 Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Abort 500 error page."""
    return render_template('error.html', error_msg="500 Internal Server error", pagetitle="500 Internal Server error"), 500