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
from flask import render_template, flash, request, redirect
from dining import app

@app.route('/')
def index():
    """Display index (home) route."""
    return render_template('index.html')
