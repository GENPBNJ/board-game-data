from flask import Flask, render_template, request, url_for, redirect
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
    # __tablename__='allboardgamedetails'
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

@app.route('/catalog')          
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
                                                # ).filter(BoardGames.domain == 'Thematic Games', BoardGames.mechanic == 'Variable Player Powers'
                                                ).order_by(BoardGames.BGG_Rank).distinct().limit(100)
    return render_template('index.html', boardgames=boardgames)


@app.route('/')
def hello():
    # boardgames = BoardGames.query.filter(BoardGames.domain == 'Thematic Games', BoardGames.mechanic == 'Dice Rolling').all()
    return render_template('home.html')

@app.route('/hello2')
def hello2():
    # boardgames = BoardGames.query.filter(BoardGames.domain == 'Thematic Games', BoardGames.mechanic == 'Dice Rolling').all()
    return render_template('home1.html')

# @app.route('/edit/<string:name>/<string:domain>/<string:mechanic>', methods=('GET', 'POST'))
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(name, domain, mechanic):
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

        boardgame.name = name
        boardgame.year_published = year_published
        boardgame.min_players = min_players
        boardgame.max_players = max_players
        boardgame.min_age = min_age
        boardgame.play_time = play_time
        boardgame.owned_users = owned_users
        boardgame.rating_average = rating_average
        boardgame.complexity = complexity
        
        db.session.add(boardgame)
        db.session.commit()

        return redirect(url_for('catalog'))

    return render_template('edit.html', boardgame=boardgame)

@app.route('/create', methods=('GET', 'POST'))
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

            boardgame = BoardGames(id=id, 
                                   name=name,
                                   year_published=year_published, 
                                   min_players=min_players, 
                                   max_players=max_players,
                                   min_age=min_age,
                                   play_time=play_time,
                                   owned_users=owned_users,
                                   rating_average=rating_average,
                                   complexity=complexity
                                )
            
            db.session.add(boardgame)
            db.session.commit()

            return redirect(url_for('catalog'))
        return render_template('create.html', boardgame=boardgame)
    except:
        return redirect(url_for('catalog'))

@app.route('/<int:id>/delete/', methods=['GET','POST'])
def delete(id):
    boardgame = BoardGames.query.filter_by(id = id).first()
    if request.method == 'POST':
        if boardgame:
            db.session.delete(boardgame)
            db.session.commit()
        return redirect(url_for('catalog'))
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

