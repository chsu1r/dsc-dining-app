"""
Dining app forms.
Forms for the webpage.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.widgets import TextArea

# https://www.youtube.com/watch?v=f_3YFEEovCc
class LoginForm(FlaskForm):
    """Form for login."""
    # Each field in the form is just another __Field object that you declare in this class.
    # Different types of fields have different types of objects you'd declare.
    # The arguments inside determine what the field should be known as (with other metadata), 
    # as well as validators on the input field. For example, the email field requires you to submit
    # a nonempty string (DataRequired()) and for the input string to be a valid email (Email("...."))
    email = StringField('Email', render_kw={"placeholder": "Email Address"},
                        validators=[DataRequired(),
                                    Email("This field requires a valid email address")])
    password = PasswordField('Password', render_kw={"type": "password", "placeholder": "Password"},
                             validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """Form for register."""
    name = StringField("Name", render_kw={"placeholder": "Name"},
                       validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email',
                        render_kw={"placeholder": "Email Address"},
                        validators=[DataRequired(),
                                    Email("This field requires a valid email address")])
    password = PasswordField('Password', render_kw={"type": "password", "placeholder": "Password"},
                             validators=[DataRequired(),
                                         EqualTo('confirm_password',
                                                 message='Passwords must match.')])
    # Note the "EqualTo" validator that forces password == confirm_password.
    confirm_password = PasswordField('Confirm Password',
                                     render_kw={"type": "password",
                                                "placeholder": "Confirm Password"},
                                     validators=[DataRequired()])
    submit = SubmitField('Register')


class ResetPasswordForm(FlaskForm):
    """Form for resetting password."""
    email = StringField('Email', render_kw={"placeholder": "Email Address"},
                        validators=[DataRequired(),
                                    Email("This field requires a valid email address")])
    submit = SubmitField('Reset')
