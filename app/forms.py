from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired
import numpy as np

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sin = FloatField('Sin(x)', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class InputForm(FlaskForm):
    A = FloatField('Amplitude (m)', default=1.0, validators=[DataRequired()])
    b = FloatField('Dampling Factor (kg/s)', default=0)
    w = FloatField('Freq (1/s)', default=2*np.pi, validators=[DataRequired()])
    T = FloatField('Time (s)', default=18.0, validators=[DataRequired()])
    #submit = SubmitField('Compute')



