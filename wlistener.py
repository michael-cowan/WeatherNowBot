import tweepy
import time
import json
import sys
import unicodedata
import scraper as WS



class WeatherListener(tweepy.streaming.StreamListener):

    def __init__(self, api):
        self.api = api

    def respond(self, user_name, msg, id = None, dm = False):
        """
            Used to send a response of the weather
        """

        # Finds answer based on message received
        ans = WS.get_weather_now(msg, dm = dm)

        # Checks to see whether msg received was a tweet or DM
        if not dm:
            self.api.update_status("@%s %s" %(user_name, ans), in_reply_to_status_id = id)
            print 'TWEET SENT\n'
        else:
            self.api.send_direct_message(screen_name = user_name, text = ans)
            print 'DM SENT\n'

    def on_connect(self):
        print 'WeatherNowBot has started\n\n'

    def on_status(self, status):
        # Checks for mentions
        if status.entities['user_mentions']:
            for u in status.entities['user_mentions']:
                if u['screen_name'] == 'WeatherNowBot':

                    sentby = status.user.screen_name
                    msg    = unicodedata.normalize('NFKD', status.text).encode('ascii', 'ignore')
                    id     = status.id

                    print 'Mention from @%s' %(sentby)

                    if 'RT' in msg:
                        msg = msg.replace('RT @' + sentby + ': ', '')
                    msg = msg.replace('@WeatherNowBot ', '')

                    # Removes other common words that aren't needed
                    msg = msg.lower()
                    msg = msg.replace(" what's ", "").replace(" what ", "").replace(" is ", "")
                    msg = msg.replace(" weather ", "").replace(" like ", "")
                    msg = msg.replace(" in ", "").replace(" today ", "")

                    self.respond(sentby, msg, id)

        return True

    def on_direct_message(self, status):
        
        dm_dict = status.direct_message

        if dm_dict[u'sender_screen_name'] != 'WeatherNowBot':

            sentby = dm_dict[u'sender_screen_name']
            msg    = unicodedata.normalize('NFKD', dm_dict[u'text']).encode('ascii', 'ignore')

            print 'DM from @%s' %(sentby)

            self.respond(sentby, msg, dm = True)

        return True

    def on_error(self, status):
        # Error is printed to console if it occurs
        print >> sys.stderr, '\nError: %s \n' %(str(status))
        return True
        print >> sys.stderr, "WeatherNowBot restarted\n"

    def on_timeout(self):
        # Prints to console if a timeout occurs and pauses stream for a minute
        print >> sys.stderr, "\nTimeout, sleeping for 60 seconds...\n"
        time.sleep(60)
        return True
        print >> sys.stderr, "WeatherNowBot restarted\n"

    def on_disconnect(self):
        return False
