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
    snr = FloatField('SNR', default=10.0, description = "SNR" ,validators=[InputRequired()])
    exptime = FloatField('Exposure Time (s)',  description = "Exposure time (s)", default=60)


class CCDForm1(FlaskForm):
    zeropoint1 = FloatField('Zeropoint', default=1521 , description="Count Rate Standard (e-/sec)", validators=[InputRequired()])
    magnitude1 = FloatField('Magnitude', default = 26, description='Target Magnitude', validators=[InputRequired()])
    pixscale1 = FloatField('Scale', default = 0.218, description='Pixel Scale (arcsec/pix)', validators=[InputRequired()])
    skyb1 = FloatField('Sky Brightness', default = 21.9, description='Sky Brightness (mag/arcsec^2)', validators=[InputRequired()])
    radius1 = FloatField('Radius', default = 1, description='Photometric Aperture Radius (arcsec)', validators=[InputRequired()])
    readnoise1 = FloatField('RN', default = 8, description='Readnoise (e-)', validators=[InputRequired()])
    gain1 = FloatField('Inverse-Gain', default = 1, description='Gain (e-/ADU)', validators=[InputRequired()])
    dark1 = FloatField('Dark Current', default=1.0, description = "Dark Current (e-/pixel/sec)" ,validators=[InputRequired()])


class CCDForm2(FlaskForm):
    zeropoint2 = FloatField('Zeropoint', default=1521 , description="Count Rate Standard (e-/sec)", validators=[InputRequired()])
    magnitude2 = FloatField('Magnitude', default = 26, description='Target Magnitude', validators=[InputRequired()])
    pixscale2 = FloatField('Scale', default = 0.218, description='Pixel Scale in arcsec/pix', validators=[InputRequired()])
    skyb2 = FloatField('Sky Brightness', default = 21.9, description='Sky Brightness (mag/arcsec^2)', validators=[InputRequired()])
    radius2 = FloatField('Radius', default = 1, description='Photometric Aperture Radius (arcsec)', validators=[InputRequired()])
    readnoise2 = FloatField('RN', default = 8, description='Readnoise in e-', validators=[InputRequired()])
    gain2 = FloatField('Inverse-Gain', default = 1, description='Gain in e-/ADU', validators=[InputRequired()])
    dark2 = FloatField('Dark Current', default=1.0, description = "Dark Current in e-/pixel/sec" ,validators=[InputRequired()])

