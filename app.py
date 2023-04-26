from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql
import secrets
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
# conn = "mysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    privilege = db.Column(db.String(20), nullable =False, default = 'user')

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': "Password"})
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': "Password"})
    
    submit = SubmitField('Login')

class BoardGames(db.Model):
    __tablename__='bgg_dataset'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String)
    year_published = db.Column(db.Integer)
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    play_time = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    complexity = db.Column(db.Double)
    owned_users = db.Column(db.Integer)
    BGG_Rank = db.Column(db.Integer)
    rating_average = db.Column(db.Double)
    domains = db.Column(db.String)
    mechanics = db.Column(db.String)

@app.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                username= request.form.get('username')
                return redirect(url_for('catalog', username=username))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/catalog')    
@login_required      
def catalog():
    boardgames = BoardGames.query.with_entities(BoardGames.id, 
                                                BoardGames.name,
                                                BoardGames.BGG_Rank, 
                                                BoardGames.year_published, 
                                                BoardGames.min_players, 
                                                BoardGames.max_players, 
                                                BoardGames.play_time, 
                                                BoardGames.min_age, 
                                                BoardGames.owned_users, 
                                                BoardGames.rating_average, 
                                                BoardGames.complexity,
                                                BoardGames.domains,
                                                BoardGames.mechanics
                                                ).order_by(BoardGames.BGG_Rank).distinct().limit(21000)
    username = request.args.get('username', None)
    users = User.query.with_entities(User.username, User.privilege).filter(User.username == 'thomas')

    return render_template('index.html', boardgames=boardgames, users=users)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required      
def edit(id):

    boardgame = BoardGames.query.filter_by(id = id).first()
    print(boardgame)
    if request.method == 'POST':
        name = request.form['name']
        year_published = request.form['year_published']
        min_players = request.form['min_players']
        max_players = request.form['max_players']
        min_age = request.form['min_age']
        play_time = request.form['play_time']
        owned_users = request.form['owned_users']
        rating_average = request.form['rating_average']
        complexity = request.form['complexity']
        domains = request.form['domains']
        mechanics = request.form['mechanics']

        boardgame.name = name
        boardgame.year_published = year_published
        boardgame.min_players = min_players
        boardgame.max_players = max_players
        boardgame.min_age = min_age
        boardgame.play_time = play_time
        boardgame.owned_users = owned_users
        boardgame.rating_average = rating_average
        boardgame.complexity = complexity
        boardgame.domains = domains
        boardgame.mechanics = mechanics
        
        db.session.add(boardgame)
        db.session.commit()

        return redirect(url_for('catalog'))

    return render_template('edit.html', boardgame=boardgame)

@app.route('/create', methods=('GET', 'POST'))
@login_required      
def create():
    if request.method == 'GET':
        return render_template('create.html')

    try:
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            year_published = request.form['year_published']
            min_players = request.form['min_players']
            max_players = request.form['max_players']
            min_age = request.form['min_age']
            play_time = request.form['play_time']
            owned_users = request.form['owned_users']
            rating_average = request.form['rating_average']
            complexity = request.form['complexity']
            domains = request.form['domains']
            mechanics = request.form['mechanics']

            boardgame = BoardGames(id=id, 
                                   name=name,
                                   year_published=year_published, 
                                   min_players=min_players, 
                                   max_players=max_players,
                                   min_age=min_age,
                                   play_time=play_time,
                                   owned_users=owned_users,
                                   rating_average=rating_average,
                                   complexity=complexity,
                                   domains=domains,
                                   mechanics=mechanics
                                )
            db.session.add(boardgame)
            db.session.commit()
            return redirect(url_for('catalog'))
        return render_template('create.html', boardgame=boardgame)
    except:
        return redirect(url_for('catalog'))

@app.route('/<int:id>/delete/', methods=['GET','POST'])
@login_required      
def delete(id):
    boardgame = BoardGames.query.filter_by(id = id).first()
    if request.method == 'POST':
        if boardgame:
            db.session.delete(boardgame)
            db.session.commit()
        return redirect(url_for('catalog'))
    return render_template('index.html')

# if __name__ == "__main__":
app.run()
