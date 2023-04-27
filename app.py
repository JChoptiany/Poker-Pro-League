from flask import Flask, render_template, flash
from forms import PlayerLoginForm, RemovePlayerForm, AddPlayerForm, AddResultForm, RenamePlayerForm, AdminLoginForm, AddMatchForm, RemoveMatchForm, LoadMatchForm, RemoveResultsForm
from Player import Player
from Result import Result
from Match import Match
from wtforms import StringField
import datetime
from DatabaseConnector import DatabaseConnector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'put_secret_key_here'

db = DatabaseConnector()


def validate_data_field(field: StringField) -> bool:
    if field.data.strip() == '':
         return False
    try:
        datetime.datetime.strptime(field.data, '%Y-%m-%d').date()
        return True
    except:
        return False


def validate_player_field(field: StringField) -> bool:
    if field.data.strip() == '':
         return False
    return db.players.is_registered(field.data)


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', number_of_players=db.players.count(), number_of_matches_played=db.get_number_of_matches(), 
    number_of_matches_scheduled=db.get_number_of_scheduled_matches(), maximum_number_of_players_in_match=db.get_maximum_players_in_match(),
    active_players_percentage=db.get_active_players_percentage(), age_gap=db.get_age_gap(), total_points=db.get_total_points(), 
    total_coins=db.get_total_coins_played())


@app.route("/schedule")
def schedule():
    return render_template('schedule.html', title="Schedule", next_match=db.get_the_next_match(), future_matches=db.get_future_matches())


@app.route("/players")
def players():
    return render_template('players.html', title="Player List", players=db.players.get_all(), number_of_players=db.players.count())


@app.route("/ranking")
def ranking():
    return render_template('ranking.html', title="Ranking", players=db.get_ranking_table(), matches_played=db.get_number_of_matches(), recent_match=db.get_recent_match_date())


@app.route("/login", methods=['GET', 'POST'])
def playerLogin():
    form = PlayerLoginForm()
    if form.validate_on_submit():
        if db.players.is_registered(form.player_name.data):
            player = db.players.get(form.player_name.data)
            if form.password.data == player.password:
                return render_template('player_statistics.html', title="Statistics", player=db.get_full_player_statistics(player), total_league_matches=db.get_number_of_matches())
            else:
                flash('Invalid password! Please try again.', 'danger')
        else:
            flash('User with given nickname does not exist!', 'danger')

    return render_template('login.html', title='Statistics', form=form)


@app.route("/admin", methods=['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == app.config['SECRET_KEY']:
            return render_template('admin_panel.html', title="Admin Panel")
        else:
            flash('Invalid password! Please try again.', 'danger')       
    return render_template('admin_login.html', title='Admin Panel', form=form)


@app.route("/addPlayer", methods=['GET', 'POST'])
def addPlayer():
    form = AddPlayerForm()
    if form.validate_on_submit(): 
        try:
            player = Player(form.first_name.data.strip(), form.last_name.data.strip(), form.date_of_birth.data.strip(), form.gender.data)
            db.players.add(player) 
            flash(f'Player {player.nickname} has been added successfully!', 'success')
        except:
            flash('An error occurred! Please try again later!', 'danger')
    else:
        flash('Cannot add new player! Please fill all the cells correctly.', 'danger')
    return render_template('add_player.html', title='Add Player', form=form)


@app.route("/removePlayer", methods=['GET', 'POST'])
def removePlayer():
    form = RemovePlayerForm()
    if form.validate_on_submit():
        if db.players.is_registered(form.nickname.data):
            if db.players.validate_date_of_birth(form.nickname.data, form.date_of_birth.data):
                try: 
                    db.remove_all_the_player_results_by_nickname(form.nickname.data)           
                    db.players.remove(form.nickname.data) 
                    flash(f'Player {form.nickname.data} has been removed successfully!', 'success')
                except:
                    flash('An error occurred! Please try again later!', 'danger')
            else:
                flash('Verification failed! Please make sure you have chosen the correct player.', 'danger')
        else:
            flash(f'There is no player named {form.nickname.data}.', 'danger')
    else:
        flash('Cannot remove player! Please fill all the cells correctly.', 'danger')
    return render_template('remove_player.html', title='Remove Player', form=form)


@app.route("/renamePlayer", methods=['GET', 'POST'])
def renamePlayer():
    form = RenamePlayerForm()
    if form.validate_on_submit():
        if db.players.is_registered(form.current_nickname.data):
            if db.players.validate_date_of_birth(form.current_nickname.data, form.date_of_birth.data):
                try: 
                    db.players.rename(form.current_nickname.data, form.new_nickname.data)
                    flash(f'Player {form.current_nickname.data} has been successfully renamed to {form.new_nickname.data}!', 'success')
                except:
                    flash('An error occurred! Please try again later!', 'danger')
            else:
                flash('Verification failed! Please make sure you have chosen the correct player.', 'danger')
        else:
            flash(f'There is no player named {form.current_nickname.data}.', 'danger')
    else:
        flash('Cannot rename player! Please fill all the cells correctly.', 'danger')
    return render_template('rename_player.html', title='Rename Player', form=form)


@app.route("/addResult", methods=['GET', 'POST'])
def addResult():
    form = AddResultForm()
    if form.validate_on_submit(): 
        player_nicknames = []
        date = datetime.date.today()
        for field in form:
            if isinstance(field, StringField):
                if validate_data_field(field):
                    date = datetime.datetime.strptime(field.data, '%Y-%m-%d').date()
                elif validate_player_field(field):
                    player_nicknames.append(field.data) 
        try: 
            results = []
            for index, nickname in enumerate(player_nicknames):
                results.append(Result(date, index+1, db.players.get(nickname)))

            db.add_results(results)
            flash(f'Results have been added successfully!', 'success')
        except:
            flash('An error occurred! Please try again later!', 'danger')
    else:
        flash('Cannot add results! Please fill all the cells correctly.', 'danger')
    return render_template('add_result.html', title='Add Result', form=form)


@app.route("/addMatch", methods=['GET', 'POST'])
def addMatch():
    form = AddMatchForm()
    if form.validate_on_submit(): 
        try:
            match = Match(datetime.datetime.strptime(form.date.data, '%Y-%m-%d %H:%M'), int(form.entry_fee.data), int(form.expected_players.data), int(form.confirmed_players.data))
            db.add_match(match)
            flash(f'Match has been added successfully!', 'success')
        except:
            flash('An error occurred! Please try again later!', 'danger')
    else:
        flash('Cannot add match! Please fill all the cells correctly.', 'danger')
    return render_template('add_match.html', title='Add Match', form=form)


@app.route("/matches")
def matches():
    return render_template('matches.html', title="Match List", matches=db.get_all_the_matches(), number_of_matches=db.get_number_of_scheduled_matches())


@app.route("/removeMatch", methods=['GET', 'POST'])
def removeMatch():
    form = RemoveMatchForm()
    if form.validate_on_submit():
        if db.validate_match_date(form.id.data, datetime.datetime.fromisoformat(form.date.data)):
            try:
                db.remove_match_by_id(form.id.data)
                flash(f'Match has been removed successfully!', 'success')
            except:
                flash('An error occurred! Please try again later!', 'danger')
        else:
            flash('Verification failed! Please make sure you are trying to remove correct match.', 'danger')
    else:
        flash('Cannot remove match! Please fill all the cells correctly.', 'danger')
    return render_template('remove_match.html', title='Remove Match', form=form)


@app.route("/removeOutdatedMatches")
def removeOutdatedMatches():    
    try:
        db.remove_outdated_matches()
        flash('Outdated matches have been removed!', 'success')
    except Exception:
        flash('Cannot remove matches!', 'danger')
    return render_template("admin_panel.html")


@app.route("/removeResults", methods=['GET', 'POST'])
def removeResults():
    form = RemoveResultsForm()
    if form.validate_on_submit():
        if form.password.data == app.config['SECRET_KEY'] and form.confirmation_text.data == "REMOVE ALL":
            try:
                db.remove_all_the_results()
                flash(f'All the results have been removed successfully!', 'success')
            except:
                flash('An error occurred! Please try again later!', 'danger')
        else:
            flash('Verification failed! Please try again.', 'danger')
    else:
        flash('Cannot remove results! Please fill all the cells correctly.', 'danger')
    return render_template('remove_results.html', title='Remove Results', form=form)


if __name__ == '__main__':
    app.run(debug=True)    
