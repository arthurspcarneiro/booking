from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from datetime import datetime


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class TradeForm2(FlaskForm):
    trade_date = DateField('Trade date', default=datetime.today(), validators=[DataRequired()])
    order = SelectField('Buy/Sell',coerce=str,choices=[("Buy","Buy"),("Sell","Sell")] )
    product = SelectField('Product',coerce=str,choices=[("call","Call"),("put","Put")] )
    code = StringField('Code', validators=[DataRequired(),Length(0, 8)])
    strategy = StringField('Strategy', validators=[DataRequired(),Length(0, 32)])
    strike = DecimalField('Strike', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(message='That\'s not a valid email address.')])
    submit = SubmitField('Book')

class TradeForm(FlaskForm):
    trade_date = DateField('Trade date', default=datetime.today())
    order = SelectField('Buy/Sell',coerce=str,choices=[("Buy","Buy"),("Sell","Sell")] )
    product = SelectField('Product',coerce=str,choices=[("call","Call"),("put","Put")] )
    code = StringField('Code', validators=[Length(5, 8)])
    strategy = SelectField('Strategy',coerce=str,choices=[("Seco","Seco"),("Strangle","Strangle"),("Straddle","Straddle"),("BullSpread","Bull Spread"),("BearSpread","Bear Spread")])
    #strategy = StringField('Strategy', validators=[Length(4, 32)])
    strike = DecimalField('Strike')
    amount = IntegerField('Amount')
    price = DecimalField('Price')
    submit = SubmitField('Book')
    
class LegForm(FlaskForm):
    order = SelectField('New trade - Number of legs:',coerce=int,choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')
