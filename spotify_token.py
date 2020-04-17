import credentials
import spotipy.util as util


def get_token(scope=None):
    username = credentials.USERNAME
    client_id = credentials.CLIENT_ID
    client_secret = credentials.CLIENT_SECRET
    redirect_uri = credentials.REDIRECT_URI
    if scope is None:
        return util.prompt_for_user_token(username=username,
                                          client_id=client_id,
                                          client_secret=client_secret,
                                          redirect_uri=redirect_uri)
    else:
        return util.prompt_for_user_token(username=username,
                                          scope=scope,
                                          client_id=client_id,
                                          client_secret=client_secret,
                                          redirect_uri=redirect_uri)
