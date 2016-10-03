import os
import re

INPUT_FOLDER = '/Users/stephenh/github/NewsDayBarometer/outlets/v_2016-10-03'

raw_file_names = os.listdir(INPUT_FOLDER)
file_names = [x for x in raw_file_names if re.search('\.csv$', x)]

categories = [x.replace('.csv', '') for x in file_names]

# data structure: dictionary with key=file name stem and value = array of dictionaries
# each dictionary is a row in the dataset

outlets = {}

for i in range(len(file_names)):
	dataset = []
	with open(os.path.join(INPUT_FOLDER, file_names[i]), 'r') as f:
		whole_file = f.readline()
		lines = whole_file.split('\r')
		for line in lines:
			fields = line.split(',')
			if fields[0] == 'Outlet':
				continue
			row = {'outlet': fields[0], 'url': fields[1], 'twitter': fields[2], 'short url': fields[3]}
			dataset.append(row)
	outlets[categories[i]] = dataset
