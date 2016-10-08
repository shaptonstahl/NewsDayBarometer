import os
import re

CATEGORY_INPUT_FOLDER = '/Users/stephenh/github/NewsDayBarometer/outlets/v_2016-10-03'

raw_file_names = os.listdir(CATEGORY_INPUT_FOLDER)
file_names = [x for x in raw_file_names if re.search('\.csv$', x)]

categories = [x.replace('.csv', '') for x in file_names]

# data structure: dictionary with key=category (stem of file name) and value = array of dictionaries
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
