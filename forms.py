from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from datetime import date
from datetime import datetime


class PlayerLoginForm(FlaskForm):
    player_name = StringField('Player name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    
class AdminLoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddPlayerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = StringField('Date', validators=[DataRequired()], render_kw={'placeholder': 'YYYY-MM-DD'})    
    gender = RadioField('Gender', choices=[('M','Male'),('F','Female')], validators=[DataRequired()])
    submit = SubmitField('Add')

class RemovePlayerForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    date_of_birth = StringField('Date', validators=[DataRequired()], render_kw={'placeholder': 'YYYY-MM-DD'})  
    confirmation = BooleanField('Are you sure, you want to remove player with all his/her results? This operation cannot be reversed.', validators=[DataRequired()])  
    submit = SubmitField('Remove')

class RenamePlayerForm(FlaskForm):
    current_nickname = StringField('Current nickname', validators=[DataRequired()])
    new_nickname = StringField('New nickname', validators=[DataRequired()])
    date_of_birth = StringField('Date', validators=[DataRequired()], render_kw={'placeholder': 'YYYY-MM-DD'})  
    submit = SubmitField('Save')

class AddResultForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()], default=date.today().strftime('%Y-%m-%d'))   
    first_place = StringField('1. Player nickname', validators=[DataRequired()])
    second_place = StringField('2. Player nickname', validators=[DataRequired()])
    third_place = StringField('3. Player nickname', validators=[DataRequired()])
    fourth_place = StringField('4. Player nickname', validators=[DataRequired()])
    fifth_place = StringField('5. Player nickname', validators=[DataRequired()])
    sixth_place = StringField('6. Player nickname', validators=[DataRequired()])
    seventh_place = StringField('7. Player nickname')
    eighth_place = StringField('8. Player nickname')
    ninth_place = StringField('9. Player nickname')
    tenth_place = StringField('10. Player nickname')
    eleventh_place = StringField('11. Player nickname')
    twelfth_place = StringField('12. Player nickname')
    submit = SubmitField('Add')

class AddMatchForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()], default=datetime.now().strftime('%Y-%m-%d %H:%m'))
    expected_players = IntegerField('Expected players', validators=[DataRequired(), NumberRange(min=0, max=20)], default=0)
    confirmed_players = IntegerField('Confirmed players', validators=[DataRequired(), NumberRange(min=0, max=20)], default=0)
    entry_fee = IntegerField('Entry fee [PLN]', validators=[DataRequired(), NumberRange(min=0, max=1000)], default=0)
    submit = SubmitField('Add')

class RemoveMatchForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()], render_kw={'placeholder': 'YYYY-MM-DD'})
    confirmation = BooleanField('Are you sure, you want to remove match from the league calendar? This operation cannot be reversed.', validators=[DataRequired()])  
    submit = SubmitField('Remove')

class LoadMatchForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Load')

class RemoveResultsForm(FlaskForm):
    password = PasswordField('Admin password', validators=[DataRequired()])
    confirmation_text = StringField('Please enter "REMOVE ALL" to confirm you want to remove all the results', validators=[DataRequired()])
    confirmation_click = BooleanField('Are you sure, you want to remove ALL THE RESULTS? This operation CANNOT be reversed.', validators=[DataRequired()])  
    submit = SubmitField('Remove')
