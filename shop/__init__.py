from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import stripe

app = Flask(__name__, template_folder='templates') # initialise flask app and set template folder
app.charset = 'utf-8'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///securecart.db' # database URI for SQLite
db = SQLAlchemy(app) # database instance

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable SQLAlchemy event system to save resources
app.config['SECRET_KEY'] = os.urandom(24) # generate a random secret key for session management
app.config['UPLOAD_FOLDER'] = "../static/images" # folder to store uploaded images

bcrypt = Bcrypt(app) # bcrypt for password hashing

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51QjgpJP8JWjkpw7dT1NpHUjKJ4MxH0EeIOFTUJ4BoOPQCOzDe8e0SyXba8XrYRkQJKKZpJc1bfxca0OjSoqVErvf00opk9ULku' # stripe public key for client-side usage
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51QjgpJP8JWjkpw7dUt5AkFTbQOuCMqdrXm6Pex2iTbZH775wzG7ofdLuhsxGXD6Xms8VWiGft4FsWSlC1tbns5b000DAkR0xBs' # stripe secret key for server-side API calls
stripe.api_key = app.config['STRIPE_SECRET_KEY'] # set stripe API key

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeKLcUqAAAAAMdxwNe-3JxPufMLhxmWc5DLyfg1' # captcha public key
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeKLcUqAAAAAAZb1nQIUZ2sOXdw_IkZivzWE_2f' # captcha private key

from shop.admin import routes

# create all the database tables
with app.app_context():
    db.create_all()