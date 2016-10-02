'''
In a sample of tweets count the number of links there are to news sites
in various categories to gauge how busy a news day it is.

1. From a sample of tweets save URLs.
2. Search URLs for those pointing to news sites.
3. Save file with sample size and counts for overall and for each category.

'''

from tweepy import StreamListener
import tweepy
import datetime
# import json
import time
import sys
# import urllib2
# import urllib
# from urlparse import urlparse
# from sets import Set
# from xml.etree import ElementTree as ET
# from lxml import etree
# import csv
# import progressbar
# import codecs
import os
import unshorten_url

WORKING_PATH = '/Users/stephenh/github/NewsDayBarometer/temp'
DATA_PATH = '/Users/stephenh/github/NewsDayBarometer/data'
CATEGORIES_FILE = '/Users/stephenh/github/NewsDayBarometer/categories.csv'
CONSUMER_KEY = 'rocvYBcGgKBfNLHHZlkCVAY6i'
CONSUMER_SECRET = 'wWlkoEYdFQf7Mrc4zDiFXAknrnfkPY0arbSjr3uRSXvBRtiTwB'
ACCESS_TOKEN_KEY = '17050800-zijJEwmbyJARHllbJutCX0S5t5MBOhhGTPKlZSf7m'
ACCESS_TOKEN_SECRET = 'WFU3FdrosBnEeZcVTbJVJfRlyJNQEHujUDUPhDxmuz2QW'
SAMPLE_SIZE = 100
# can stream about 1000 / minute

temp_file_no_extension = WORKING_PATH + '/' + datetime.datetime.now().strftime('%F_%H-%M-%S')
temp_stream_file = temp_file_no_extension + '.csv'
temp_unshortened_file = temp_file_no_extension + '_unshortened.csv'

if not os.path.exists(WORKING_PATH):
	os.makedirs(WORKING_PATH)

if not os.path.exists(DATA_PATH):
	os.makedirs(DATA_PATH)

class listener(StreamListener):
	def __init__(self, api = None, n_tweets_to_collect = 10, output_filename = None):
		self.api = api
		self.n_tweets_to_collect = n_tweets_to_collect
		self.n_tweets_collected = 0
		self.f = open(output_filename, 'w+')
	
	def on_status(self, status):
		self.n_tweets_collected += 1
		try:
			self.f.write(status.entities['urls'][0]['expanded_url'].encode('utf-8') + '\n')
		except:
			pass
		if self.n_tweets_collected >= self.n_tweets_to_collect:
			self.f.close()
			return False

#initialize twitter api
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#begin streaming tweets
print 'Fetching sample of tweets'

stream = tweepy.streaming.Stream(auth, listener(api, SAMPLE_SIZE, temp_stream_file))
print 'Streaming started...'

try:
	stream.sample(languages=['en'])
except IOError as e:
	print e.strerror
except:
	print sys.exc_info()[0]
	print 'error!'
	stream.disconnect()

# unshorten the urls
print 'Unshortening the urls...'
with open(temp_stream_file, 'r') as f_in:
	with open(temp_unshortened_file, 'w') as f_out:
		for url in f_in:
			unshortened_url = unshorten_url.unshorten_url(url)
			if unshortened_url:
				f_out.write(unshortened_url + '\n')
