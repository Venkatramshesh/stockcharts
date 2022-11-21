from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


##WTForm
class SubmitForm(FlaskForm):
    tickersymbol = StringField(label='Ticker/Symbol')
    submit = SubmitField(label='Submit')
