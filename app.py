from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
# conn = "mysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class BoardGames(db.Model):
    __tablename__='allboardgamedetails'
    name = db.Column(db.String, primary_key = True, nullable = False)
    year_published = db.Column(db.Integer)
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    play_time = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    complexity = db.Column(db.Double)
    owned_users = db.Column(db.Integer)
    bgg_rank = db.Column(db.Integer)
    rating_average = db.Column(db.Double)
    domain = db.Column(db.String, primary_key = True)
    mechanic = db.Column(db.String, primary_key = True)

@app.route('/dashboard')          
def dashboard():
    return render_template('index.html')


@app.route('/')
def hello():
    # boardgames = BoardGames.query.filter(BoardGames.domain == 'Thematic Games', BoardGames.mechanic == 'Dice Rolling').all()
    boardgames = BoardGames.query.distinct().all()
    return render_template('index.html', boardgames=boardgames)


if __name__ == "__main__":
    app.run()

