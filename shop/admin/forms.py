from wtforms import *
from wtforms.validators import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


# form used for registering customers
class RegistrationForm(FlaskForm):
    name = StringField("First Name", [DataRequired(), Length(min=4, max=25)])
    surname = StringField("Surname", [DataRequired(), Length(min=4, max=25)])
    username = StringField("Username", [DataRequired(), Length(min=4, max=25)])
    email = EmailField("Email Address", [DataRequired(), Length(min=4, max=100)])
    password = PasswordField("New Password", [DataRequired()])
    confirm = PasswordField("Repeat Password", [DataRequired()])


# form used for registering customers
class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(min=4, max=25)])
    password = PasswordField("New Password", [DataRequired()])


# form used for registering admins
class AdminRegistrationForm(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(min=4, max=25)])
    email = EmailField("Email Address", [DataRequired(), Length(min=6, max=35)])
    password = PasswordField("New Password", [DataRequired()])
    confirm = PasswordField("Repeat Password", [DataRequired()])


# form used for adding products
class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = IntegerField("Price (£)", validators=[DataRequired()])
    image_url = FileField(
        "Product Image",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
