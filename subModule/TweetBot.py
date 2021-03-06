import sys, tweepy
import time
import _thread
import telepot
import TelegramBot as TB
TOKEN = sys.argv[1]  # get token from command-line
teleBot = telepot.Bot(TOKEN)

class TweetBot:
    def __init__(self, keys, user_id):
        self._consumer_key = keys[0]
        self._consumer_secret = keys[1]
        self._access_token = keys[2]
        self._access_secret = keys[3]

        try:
            auth = tweepy.OAuthHandler(self._consumer_key,
                                       self._consumer_secret)
            auth.set_access_token(self._access_token, self._access_secret)

            self.client = tweepy.API(auth)
            if not self.client.verify_credentials():
                raise tweepy.TweepError
        except tweepy.TweepError as e:
            print('ERROR : connection failed. Check your OAuth keys.')
            if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
                print('Thread is sleeping for 5 mins!')
                time.sleep(60 * 5)  # Sleep for 5 minutes
                print('Thread is starting again')
            else:
                print(e)
                print('Thread is sleeping for 5 mins')
                time.sleep(60 * 5)  # Sleep for 5 minutes
                print('Thread is starting again')
        else:
            print('Connected as @{}, you can start to tweet !'.format(self.client.me().screen_name))
            self.client_id = user_id

    def get_last_tweet(self,my_string):
        prev_tweet = None
        while True:
            try:
                tweet = self.client.user_timeline(id = self.client_id, count = 1)[0]
                if prev_tweet != tweet.text:
                    print(tweet.id)
                    print(tweet.text)
                    prev_tweet = tweet.text
                    if prev_tweet != None:
                        TB.sendToTelebot(tweet.text)
            except tweepy.TweepError as e:
                time.sleep(60 * 10)
                print('Tweepy Error')
                print(e)
                continue
            except AttributeError:
                time.sleep(60 * 10)
                print('AttributeError')
                continue
