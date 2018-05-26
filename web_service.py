# Task : Webservice providing algorithms micro services to UI interations
# Date : 10 Dec 2016
# Version : 1.0 
# Author : Vigneshwer

# Importing flask modules
from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask.ext.cors import CORS, cross_origin

# Algos module
from algos_v1 import entry_point
from algos_v1 import entry_point2

app = Flask(__name__)

cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def api_root():
    return 'Welcome to iUser Web Service'

@app.route('/process_data', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_process_data():
    if request.headers['Content-Type'] == 'application/json':
    	req = request.json
    	audio_location = req['audio_location']
        target_lang = req['target_lang']
        print str(audio_location)
        print str(target_lang)
        # Call the algos function
        process_data = entry_point(str(audio_location),str(target_lang))
        return json.dumps(process_data)
    else:
        return 'No audio_location found in args'

@app.route('/text_conv', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_text_conv():
    if request.headers['Content-Type'] == 'application/json':
        req = request.json
        text_details = req['text']
        tar_lang = req['target_lang']
        org_lang = req['org_lang']
        print str(text_details)
        print str(tar_lang)
        print str(org_lang)
        # Call the algos function
        process_data_1 = entry_point2(str(text_details),str(org_lang),str(tar_lang))
        return json.dumps(process_data_1)
    else:
        return 'No text found in args'

# # Main functions
if __name__ == '__main__':
    app.run(debug=True)