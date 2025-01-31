from wtforms import *
from wtforms.validators import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.recaptcha import RecaptchaField

# form used for registering customers
class RegistrationForm(FlaskForm):
    name = StringField('First Name', [DataRequired(), Length(min=4, max=25)])
    surname = StringField('Surname', [DataRequired(), Length(min=4, max=25)])
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email Address', [DataRequired(), Length(min=4, max=100)])
    password = PasswordField('New Password', [DataRequired()])
    confirm = PasswordField('Repeat Password', [DataRequired()])
    recaptcha = RecaptchaField()

# form used for registering customers
class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    password = PasswordField('New Password', [DataRequired()])
    recaptcha = RecaptchaField()

# form used for registering admins
class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email Address', [DataRequired(), Length(min=6, max=35)])
    password = PasswordField('New Password', [DataRequired()])
    confirm = PasswordField('Repeat Password', [DataRequired()])
    recaptcha = RecaptchaField()

# form used for adding products
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = IntegerField('Price (£)', validators=[DataRequired()])
    image_url = FileField('Product Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

'''
# form used for making payments
class PaymentForm(FlaskForm):
    name = StringField("Cardholder's Name", validators=[DataRequired()], render_kw={"placeholder": "Enter the name as it appears on the card"})
    number = IntegerField("Card Number", validators=[DataRequired(), NumberRange(min=10**15, max=10**16 - 1, message="Card number must be 16 digits")], render_kw={"placeholder": "Enter your 16-digit card number"})
    cvc = IntegerField("CVV/CVC", validators=[DataRequired(), NumberRange(min=100, max=9999, message="CVV/CVC must be 3 or 4 digits")], render_kw={"placeholder": "Enter the 3 or 4-digit security code"})
    expiration_date = StringField("Expiration Date (MM/YY)", validators=[DataRequired(), Regexp(r'^(0[1-9]|1[0-2])\/\d{2}$', message="Expiration date must be in MM/YY format")], render_kw={"placeholder": "MM/YY"})
    billing_address = StringField("Billing Address", validators=[DataRequired()])
    zip_code = StringField("Postcode", validators=[DataRequired(), Regexp(r'^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$', message="Enter a valid UK postcode")])
    submit = SubmitField("Submit Payment")
'''