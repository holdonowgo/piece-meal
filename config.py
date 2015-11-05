import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# app.config['OAUTH_CREDENTIALS'] = {
#     'facebook': {
#         'id': '470154729788964',
#         'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
#     },
#     'twitter': {
#         'id': '3RzWQclolxWZIMq5LJqzRZPTl',
#         'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
#     },
#     'google': {
#         'id': '201064811373-3qa3vnp6nsa8v5lguc9okbrrfgr9o1ep.apps.googleusercontent.com',
#         'secret': 'mLNiRQ1CQdCKW_EpC4oKJz0h'
#     }
# }

GOOGLE_LOGIN_CLIENT_ID = "447809935344-sr6gr2nqios2dq8o3jl1aph7gqohee2g.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "JyuNTsve3lzwxwZs-4QiaW66"

OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}
