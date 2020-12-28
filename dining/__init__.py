"""
Dining app __init__.
This prepares the Flask info (the main app, config variables, loads the routes in from the routes subdirectory)
"""
import os
from flask import Flask
from local_settings import Config

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is meh, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/0.12/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import dining.routes # noqa: E402  pylint: disable=wrong-import-position