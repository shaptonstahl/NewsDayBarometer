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

WORKING_PATH = '/Users/stephenh/github/NewsDayBarometer/temp'
DATA_PATH = '/Users/stephenh/github/NewsDayBarometer/data'
CATEGORIES_FILE = '/Users/stephenh/github/NewsDayBarometer/categories.csv'
CONSUMER_KEY = 'rocvYBcGgKBfNLHHZlkCVAY6i'
CONSUMER_SECRET = 'wWlkoEYdFQf7Mrc4zDiFXAknrnfkPY0arbSjr3uRSXvBRtiTwB'
ACCESS_TOKEN_KEY = '17050800-zijJEwmbyJARHllbJutCX0S5t5MBOhhGTPKlZSf7m'
ACCESS_TOKEN_SECRET = 'WFU3FdrosBnEeZcVTbJVJfRlyJNQEHujUDUPhDxmuz2QW'
SAMPLE_SIZE = 1

temp_stream_file = WORKING_PATH + '/' + datetime.datetime.now().strftime('%F_%H-%M-%S') + '.json'

if not os.path.exists(WORKING_PATH):
	os.makedirs(WORKING_PATH)

if not os.path.exists(DATA_PATH):
	os.makedirs(DATA_PATH)

def MyStreamListener(StreamListener):
#    def __init__(self, api = None, sample_size = 5, temp_file = None):
	def __init__(self, api = None):
		self.api = api or API()
		self.counter = 0
		# self.sample_size = sample_size
		self.sample_size = 2
		# self.temp_file = temp_file
		self.output = open(temp_stream_file,'w+')
	
	def on_data(self, data):
    	#this function checks data for validity
		
		#turns off the stream once we hit tweet_max
		if self.counter >=self.sample_size:
			return False
		if 'in_reply_to_status' in data:
			self.on_status(data)
		return
	
	def on_status(self,status):
		#this functions processes each individual tweet
		self.output.write(status+'\n')
		self.counter += 1
		if self.counter >= self.sample_size:
			self.output.close()
			return False
		else:
			return True
	
	def on_limit(self, track):
		sys.stderr.write(track+'\n')
		return
	
	def on_error(self, status_code):
		sys.stderr.write('Error: '+str(status_code)+'\n')
		return False
	
	def on_timeout(self):
		sys.stderr.write('Timeout, sleeping for 60 seconds...\n')
		time.sleep(60)
		return

#initialize twitter api
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#begin streaming tweets
print 'Fetching sample of tweets'

#listen = MyStreamListener(api, sample_size = SAMPLE_SIZE, temp_file = temp_stream_file)
listen = MyStreamListener(api)
stream = tweepy.streaming.Stream(auth, listen)
print 'Streaming started...'

try:
	# let's try this without a 'track' parameter
	stream.filter(track='machinelearning')
except IOError as e:
	print e.strerror
except:
	print sys.exc_info()[0]
	print 'error!'
	stream.disconnect()
