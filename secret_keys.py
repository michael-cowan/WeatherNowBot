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


consumer_key = 'BKlE8nLI2dtOzA8Cl50reKRQ9'
consumer_secret = 'XFL0wwOHOeDafYmCrHt0NVbH1m9aAPwVmEaUBzHWB85Rj9jZ2R'

access_token = '817128668120092673-sjrRaAs8Y19a5BjjkdZL81bQUzYm0Ll'
access_token_secret = '1RjGtnZ7voVUkeLQK5CeNgWNnsMwlX0e6ok8hPEx2byui'

