from app import *

with app.app_context():

    # newDomain = Domains(domain_id ='111', domain='testing')
    # db.session.add(newDomain)
    # db.session.commit()

    print('wargames'.domain_id)
    print(BoardGames.query.all())