from tweepy import StreamListener
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN_KEY"), os.getenv("ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth)


class Listener(StreamListener):
    def __init__(self, api=None, n_tweets_to_collect=10, output_filename=None):
        self.api = api
        self.n_tweets_to_collect = n_tweets_to_collect
        self.n_tweets_collected = 0
        self.f = open(output_filename, "w+")

    def on_status(self, status):
        self.n_tweets_collected += 1
        try:
            self.f.write(
                status.entities["urls"][0]["expanded_url"].encode("utf-8") + "\n"
            )
        except:
            pass
        if self.n_tweets_collected >= self.n_tweets_to_collect:
            self.f.close()
            return False


twitterStream = tweepy.streaming.Stream(auth, Listener(api, 15, "test_tweet_data.txt"))
twitterStream.sample(languages=["en"])
