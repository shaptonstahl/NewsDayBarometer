from tweepy import StreamListener
import tweepy
import json
import pickle

CONSUMER_KEY = 'rocvYBcGgKBfNLHHZlkCVAY6i'
CONSUMER_SECRET = 'wWlkoEYdFQf7Mrc4zDiFXAknrnfkPY0arbSjr3uRSXvBRtiTwB'
ACCESS_TOKEN_KEY = '17050800-zijJEwmbyJARHllbJutCX0S5t5MBOhhGTPKlZSf7m'
ACCESS_TOKEN_SECRET = 'WFU3FdrosBnEeZcVTbJVJfRlyJNQEHujUDUPhDxmuz2QW'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class Listener(StreamListener):
	def __init__(self, api = None, n_tweets_to_collect = 10, output_filename = None):
		self.api = api
		self.n_tweets_to_collect = n_tweets_to_collect
		self.n_tweets_collected = 0
		self.f = open(output_filename, 'w+')
	
	def on_status(self, status):
		try:
			self.f.write(status.entities['urls'][0]['expanded_url'].encode('utf-8') + '\n')
			self.n_tweets_collected += 1
		except:
			pass
		if self.n_tweets_collected >= self.n_tweets_to_collect:
			self.f.close()
			return False

twitterStream = tweepy.streaming.Stream(auth, Listener(api, 15, 'test_tweet_data.txt'))
# twitterStream.filter(track = 'http')
twitterStream.sample(languages=['en'])


# need to figure out how to store the expanded_url instead of the text of the tweet
# If possible, limit to English tweets
# maybe use .encode('punycode')