from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        # user = User.query.filter_by(username=username_to_check)
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please use a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please use a different email address')

    # username = StringField(label='username')
    # username = StringField(label='Username:')
    # username = StringField(label='Username:', validators=Length(min(2), max(30)))
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])

    # email_address = StringField(label='email')
    # email_address = StringField(label='Email Address:')
    # email_address = StringField(label='Email Address:', validators=Email())
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])

    # password1 = PasswordField(label='password1')
    # password1 = PasswordField(label='Enter Password:')
    # password1 = PasswordField(label='Enter Password:', validators=Length(min(6)))
    password1 = PasswordField(label='Enter Password:', validators=[Length(min=6), DataRequired()])

    # password2 = PasswordField(label='password2')
    # password2 = PasswordField(label='Confirm Password:')
    # password2 = PasswordField(label='Confirm Password:', validators=EqualTo('password1'))
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])

    # submit = SubmitField(label='submit')
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')