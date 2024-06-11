from flask_oauthlib.client import OAuth
from flask import session


def init_app(app):
    oauth = OAuth(app)
    google = oauth.remote_app(
       'google',
       consumer_key=app.config['GOOGLE_CLIENT_ID'],
       consumer_secret=app.config['GOOGLE_CLIENT_SECRET'],
       request_token_params={
           'scope': 'email profile openid',
       },
       base_url='https://www.googleapis.com/oauth2/v1/',
       request_token_url=None,
       access_token_method='POST',
       access_token_url='https://accounts.google.com/o/oauth2/token',
       authorize_url='https://accounts.google.com/o/oauth2/auth'
    )

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')
