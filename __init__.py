'''
    All imports and confugurations for the flask app is stored here.
'''

import os
import random

from flask import Flask, render_template, request, redirect, typing as ft, url_for, flash, abort
from flask_wtf.csrf import CSRFProtect
from flask.views import View
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_required, login_url, logout_user, login_user, current_user
# from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from whitenoise import WhiteNoise

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import smtplib

from email_password_regex_check import is_valid_password
from WTF_Forms.user_forms import SignUpForm, EditProfileForm, LoginForm, ChangeProfilePictureForm, ChangePasswordForm
from WTF_Forms.blog_forms import AddBlogForm, EditBlogFrom, AddCommentForm, SearchByAuthorForm, SearchByBlogTitleForm
import models
from models import Blog, User, Comment

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://josephkorede36:Korede036@cluster0.y8hkcjc.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# setting up csrf
csrf = CSRFProtect(app)

# setting up ckeditor
app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)

# setting up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)

# setting up file_upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = f'static/media/profile_pictures'

# configuring whitenoise for static files
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

def allowed_file(filename):
    '''Function to check if a file is allowed'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# ----------------------- DATABASE CONFIG ------------------------- #

database = models.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/blogglobe_db'
database.init_app(app)

# crate all tables
with app.app_context():
    database.create_all()

session = database.session


# ------------------------------ DATE -------------------------------- #

def get_date():
    date_posted = datetime.now().strftime('%d %B, %Y | %H:%M')
    return date_posted


# --------------------- USER CONFIG -------------------------- #

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(str(user_id))