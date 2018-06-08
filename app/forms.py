from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, RadioField
from wtforms.validators import DataRequired, InputRequired
import numpy as np

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sin = FloatField('Sin(x)', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class InputForm(FlaskForm):
    A = FloatField('Amplitude (m)', default=1.0, description = "Amplitude algo" ,validators=[InputRequired()])
    b = FloatField('Dampling Factor (kg/s)',  description = "Damp the thing", default=0)
    w = FloatField('Freq (1/s)', description = "Hertz" ,default=2*np.pi, validators=[InputRequired()])
    T = FloatField('Time (s)', description = "Self Explanatory" ,default=18.0, validators=[InputRequired()])

    #submit = SubmitField('Compute')

class SNRtimeForm(FlaskForm):
    snr = FloatField('SNR', default=1.0, description = "SNR" ,validators=[InputRequired()])
    exptime = FloatField('ExpTime',  description = "Exposure time", default=0)





