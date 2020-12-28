"""
Configuration Settings.
"""
import os

class Config():
    """Config object for secret keys."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', None)
    TESTING = os.environ.get('TESTING', False)
    PRODUCTION = os.environ.get('AMPLIFY_PRODUCTION_VERSION', False)
    STAGING = os.environ.get('STAGING', False)