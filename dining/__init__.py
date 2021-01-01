"""
Dining app __init__.
This prepares the Flask info (the main app, config variables, loads the routes in from the routes subdirectory)
"""
import os
from flask import Flask
from local_settings import Config
import pyrebase

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

class FirebaseAccess:
    """Setup for firebase refs. This is a wrapper class that makes it easier to use the Firebase database system via Pyrebase. """

    def __init__(self, firebase_db):
        self.root = firebase_db.ref()
        self.users = firebase_db.child("users").ref()


# TODO(SESSION1): Uncomment the Firebase stuff here.

# firebase_config = {
#     "apiKey": Config.FIREBASE_API_KEY,  # IMPORTANT - Do not paste your API key in here. We load in the API key from the Config object, which read it in from your environment variables.
#     "authDomain": "dsc-dining-app.firebaseapp.com",  # TODO(SESSION1): REPLACE ALL values with your own Firebase config values.
#     "projectId": "dsc-dining-app", 
#     "storageBucket": "dsc-dining-app.appspot.com",
#     "messagingSenderId": "775899941425",
#     "appId": "1:775899941425:web:408ce62ab569c9d4e2e310",
#     "measurementId": "G-743CR2WNPQ"
# }
# firebase = pyrebase.initialize_app(firebase_config)
# firebase_auth = firebase.auth()
# firebase_db = FirebaseAccess(firebase.database())
firebase_auth, firebase_db = None, None  # TODO(SESSION1): DELETE THIS LINE once you've finished with above.


# Tell our app about views and model.  This is dangerously close to a
# circular import, which is meh, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/0.12/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import dining.routes # noqa: E402  pylint: disable=wrong-import-position