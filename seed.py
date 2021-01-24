from models import connect_db, db, User

def seed_db(app):
    connect_db(app)
    db.drop_all()
    db.create_all()

    for user in range(4):
        user = User()
        db.session.add(user)
    db.session.commit()
    