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
import re
import unshorten_url

# set CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
import twitter_credentials

WORKING_PATH = '/Users/stephenh/github/NewsDayBarometer/temp'
DATA_PATH = '/Users/stephenh/github/NewsDayBarometer/counts'
CATEGORY_INPUT_FOLDER = '/Users/stephenh/github/NewsDayBarometer/outlets/v_2016-10-03'
SAMPLE_SIZE = 10000
# can stream about 1000 / minute
# unshortening takes...?
# total: about 1000 / 5 minutes

temp_file_no_extension = WORKING_PATH + '/' + datetime.datetime.now().strftime('%F_%H-%M-%S')
temp_stream_file = temp_file_no_extension + '.csv'
temp_unshortened_file = temp_file_no_extension + '_unshortened.csv'
output_filename = DATA_PATH + '/counts_' + datetime.datetime.now().strftime('%F') + '.csv'

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
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN_KEY, twitter_credentials.ACCESS_TOKEN_SECRET)

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

print 'Sample of ' + str(SAMPLE_SIZE) + ' tweets collected'

# unshorten the urls
print 'Unshortening the urls...'
with open(temp_stream_file, 'r') as f_in:
	with open(temp_unshortened_file, 'w') as f_out:
		for url in f_in:
			unshortened_url = unshorten_url.unshorten_url(url)
			if unshortened_url:
				f_out.write(unshortened_url + '\n')

# read outlets
raw_file_names = os.listdir(CATEGORY_INPUT_FOLDER)
file_names = [x for x in raw_file_names if re.search('\.csv$', x)]

categories = [x.replace('.csv', '') for x in file_names]

# data structure: dictionary with key=file name stem and value = array of dictionaries
# each dictionary is a row in the dataset
outlets = {}

for i in range(len(file_names)):
	dataset = []
	with open(os.path.join(CATEGORY_INPUT_FOLDER, file_names[i]), 'r') as f:
		whole_file = f.readline()
		lines = whole_file.split('\r')
		for line in lines:
			fields = line.split(',')
			if fields[0] == 'Outlet' or fields[0] == '':
				continue
			row = {'outlet': fields[0], 'url': fields[1], 'twitter': fields[2], 'short url': fields[3]}
			dataset.append(row)
	outlets[categories[i]] = dataset

def check_url_against_category(url, category):
	url_parts = [x['url'] for x in outlets[category]]
	url_in_category = False
	for url_part in url_parts:
		url_part_re = url_part.replace('.', '\\.').replace('/', '\\/')
		if re.search(url_part_re, url):
			url_in_category = True
	return url_in_category

print 'Checking urls against list of media outlets...'
counts = {}
for category in categories:
	counts[category] = 0

with open(temp_unshortened_file, 'r') as f_unshortened:
	for line in f_unshortened:
		for category in categories:
			if check_url_against_category(line, category):
				counts[category] += 1

with open(output_filename, 'w') as f_out:
	f_out.write('sample size,' + str(SAMPLE_SIZE) + '\n')
	for k, v in counts.iteritems():
		f_out.write(k + ',' + str(v) + '\n')

print 'Complete\n'