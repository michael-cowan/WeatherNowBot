"""
    #### TO FIND KEYS AND SECRETS ####

    # Consumer key and secret found in your twitter app's settings
    import tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # To find access_token and secret:
    url = auth.get_authorization_url()
    pin = <code from url>
    access_token, access_token_secret = auth.get_access_token(verifier = pin)
"""


consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

