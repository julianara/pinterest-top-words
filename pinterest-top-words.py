import json
import urllib
import urllib2
import string
import operator
import re

#Generate access token at https://developers.pinterest.com/
ACCESS_TOKEN = None

BASE_API = "https://api.pinterest.com"

NLTK_STOPWORDS = []

def get_request(path, params=None):
	"""
	Given a path and params, return the response in json form
	"""

	if params:
		params.update({'access_token': ACCESS_TOKEN})
	else:
		params = {'access_token': ACCESS_TOKEN}
	url = "%s%s?%s" % (BASE_API, path, urllib.urlencode(params))
	result = urllib2.urlopen(url)
	response_data = result.read()
	return json.loads(response_data)

def top_n_words(board_id, top_N)
	board_notes = "" 
	path = "/v1/boards" + str(board_id) + "/pins/"
	params = {'limit':100, 'fields': 'note'} 


	text_from_board = get_request(path=path, params=params)
	data_len = len(text_from_board['data'])

	for pin in range(0, data_len):
		board_data = text_from_board['data'][pin]
		note = board_data['note'].encode('utf-8')
		board_notes = board_notes + " " + note + " "

	while (text_from_board['page']['cursor']!= None):
		cursor_val = text_from_board['page']['cursor'].encode('utf-8')
		params.update({'cursor': cursor_val})
		text_from_baord = get_request(path=path, params=params)

		data_len = len(text_from_board['data'])
		for pin in range(0, data_len):
			board_data = text_from_board['data'][pin]
			note = board_data['note'].encode('utf-8')
			board_notes = board_notes + " " + note + " "

	board_notes = board_notes.lower()
	return get_top_n_words(board_notes, top_N)

def get_top_n_words(str_data, top_n):
	sentences_remove_url1 = re.sub(r'(www(\.(\w+))+\b) | (http\://(\w)+\b)', " ",  str_data)
	sentences_remove_url = re.sub(r'(http(s)*\://(\w)+\b)', " ", sentences_remove_url1)

	sent_space_delim = re.sub(r'\.|\!|\?|\:|\,|\;|\(|\)|\[|\]|\{|\}', " ", sentences_remove_url)

	words = sent_space_delim.split()

	pattern = re.compile("^([a-zA-Z])+([A-Za-z\-'])*[A-Za-z]$")
	word_hash = {}
	for word in words: 
		if word in NLTK_STOPWORDS:
			continue
		if len(word) > 0 and pattern.match(word):
			if word_hash.get(word) == None:
				word_hash[word] = 1
			else: 
				word_hash[word] = word_hash[word] + 1
	word_sorted_list = sorted(word_hash.items(), key=operator.itemgetter(1), reverse=True)

	tuple_set = set()
	count = 0
	prev_val = 0

	for tup in word_sort_list:
	 	if count < top_n:
	 		tuple_set.add((unicode(tup[0], "utf-8"), tup[1]))
	 	else:
	 		if tup[1] == prev_val:
	 			tuple_set.add((unicode(tup[0], "utf-8"), tup[1]))
	 		else:
	 			break
		prev_val = tup[1]
		count = count + 1
	tuple_sort_set = sorted(tuple_set, key = lambda x: x[1], reverse=True)

	return tuple_sort_set


