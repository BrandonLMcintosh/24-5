from models import connect_db, User


def seed_db(app):

    for user in range(4):
        user = User.register(
            form=None,
            username=f'user{user}',
            password=f'password{user}',
            email=f'user{user}@testmail.com',
            first_name=f'first_name{user}',
            last_name=f'last_name{user}')
