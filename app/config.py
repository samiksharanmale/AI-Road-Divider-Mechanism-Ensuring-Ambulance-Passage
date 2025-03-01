import os

SECRET_KEY = os.urandom(24).hex()  # Randomly generated secure key
DEBUG = True
UPLOAD_FOLDER = 'data/raw/'
