from secret_keys import *
from wlistener import *
import tweepy

def connect():
    if consumer_key and consumer_secret and access_token and access_token_secret:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Creates api object
        api = tweepy.API(auth, wait_on_rate_limit = True)

        return api
    else:
        raise KeyError("Missing authorization info. Please make sure secret_keys.py is correctly populated.")

def start_bot():
    api = connect()

    # Use Listener instance to initialize a stream
    wlistener = WeatherListener(api)

    # Initialize stream object
    my_stream = tweepy.Stream(auth = api.auth, listener = wlistener)

    # Begin the stream
    my_stream.userstream()



# tz_long

if __name__ == '__main__':
    start_bot()