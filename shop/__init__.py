import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import stripe

app = Flask(__name__, template_folder="templates")
app.charset = "utf-8"

# use env variables for configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/securecart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "securecart_secret_key")
app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "images")

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Stripe configuration
app.config["STRIPE_PUBLIC_KEY"] = os.environ.get("STRIPE_PUBLIC_KEY")
app.config["STRIPE_SECRET_KEY"] = os.environ.get("STRIPE_SECRET_KEY")
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

# reCAPTCHA configuration
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPTCHA_PRIVATE_KEY")

# import routes after app creation to avoid circular imports
from shop.admin.routes import *

with app.app_context():
    db.create_all()
