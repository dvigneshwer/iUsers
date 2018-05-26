# Task : Main functions of iUser which does language translations, speech to text and community based decision model
# Date : 10 Dec 2016
# Version : 0.1
# Author : Vigneshwer

# importing modules
import requests
import json
from google.cloud import translate
import unicodedata
import sys
import pickle
# ML modules
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics

reload(sys)
sys.setdefaultencoding('utf8')

# Function converting speech to text 
def speech_2_text(audio_location):
	url = "https://api.wit.ai/speech"
	headers = {
	    'authorization': "Bearer ****************",
	    'content-type': "audio/wav",
	    'cache-control': "no-cache",
	    'postman-token': "ad7f8d5a-0d50-a751-2b1a-895c1b8bfbbd"
	    }
	data = open(str(audio_location),'rb').read()
	response = requests.request("POST", url, data=data ,headers=headers)
	print response.text
	return response.json()

# Identify language
def identify_lang(audio_loc):
	id = 'en'
	print "The language id is " + str(id)
	return id

# Convert to corresponding localized text 
def text_converter(input_text,lang_id,target_id):
	translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.

	url = "https://translation.googleapis.com/language/translate/v2"
	api_token = "*******************"
	payload = {  
				'q': str(input_text) ,
				'source': lang_id,
				'target': target_id,
				'format': 'text'
			  }

	headers = {
	    'authorization': "Bearer "+str(api_token),
	    'content-type': "application/json",
	    'cache-control': "no-cache",
	    'postman-token': "867863ca-6f80-1358-7811-fc81a1974b66"
	    }

	response = requests.request("POST", url, data=str(payload), headers=headers)
	# print response.json()
	return response.json()

#Model trained on whatsapp community data
def community_model(input_text):
	classifier = pickle.load(open("./model/community_classifier.p","rb"))
	result = classifier.predict([input_text])
	return result

#Model which helps in making a decision
def  decision_making(final_decision):
	if final_decision[0] == str(1):
		return "Hi There !! This is a cycling group where people plan trips & discuss about gears"
	elif final_decision[0] == str(2):
		return "The next tour is this Saturday at 17th December, please contact @dvigneshwer"
	elif final_decision[0] == str(3):
		return "Visit Hoodi Decathlon to buy this gear"
	else:
		return "Plese try again"

def entry_point(audio_location,target_lang):
	# Converting audio to speech
	# audio_location = "./lang_data/english/english_sample.wav"
	response = speech_2_text(audio_location)
	print "The converted text is :- " + str(response["_text"])
	converted_text = str(response["_text"])

	# Identifying language
	lang_id = identify_lang(audio_location)
	target_id = target_lang
	print "The target language is :- " + str(target_id)

	#Convert to localized contents
	localized_content = text_converter(converted_text,lang_id,target_id)
	message = localized_content['data']['translations'][0]['translatedText']
	print "The localized content is " + str(message)

	#Community Model
	final_decision = community_model(str(converted_text))

	#Decision making - 3rd output
	decision_made = decision_making(final_decision)
	print "The decision made is" + str(decision_made)
	# Procssed data to client in json format
	processed_data = {}
	processed_data['Speech_2_text']=converted_text
	processed_data['Localized_content']=str(message)
	processed_data['Decision']=str(decision_made)

	# print type(processed_data)
	# print processed_data
	return processed_data


