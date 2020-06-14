from flask import render_template, request, redirect, url_for, Flask
import traceback
import pandas as pd
import logging

import sys
sys.path.insert(0, '../src')
from query_RDS import *

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
config_app = config['app']

# set up logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)

app.config.from_pyfile('../config/flask_config.py')

# loadthe initial app page
@app.route('/',endpoint = 'index')
def index():

    try:
        return render_template('index.html')
    except:
        traceback.print_exc()
        return render_template('error.html')

# load the results page
@app.route('/add', methods=['GET','POST'], endpoint = 'get_entry')
def get_entry():

    try:
        # get data
        airport = request.form['Airport']
        weekday = request.form['Weekday']
        month = request.form['Month']
        airline = request.form['Airline']
        state = request.form['State']

        # create dictionary for features
        airlines = config_app['airlines']
        airports = {'Midway':'13232', 'O\'Hare':'13930'}
        weekdays = config_app['weekdays']
        months = config_app['months']
        states = config_app['states']

        #translate input to data codes
        airline = airlines[airline]
        weekday = weekdays[weekday]
        month = months[month]
        state = states[state]
        airport = airports[airport]
        
        logging.info("Input airline of %s, weekday of %s, month of %s, state: %s, and airport: %s", airline, weekday, month, state, airport)

        # get prediction from RDS
        pred = pd.DataFrame(queryRDS(month,weekday,airline,airport,state))
        cancellation = pred['cancel_pred'].tolist()[0]
        delay = pred['delay_pred'].tolist()[0]

        # return results template
        return render_template('result.html', airport = airport, weekday = weekday, month = month, airline = airline, state = state, cancellation = cancellation, delay = delay)
    except:
        return render_template('error.html')



if __name__ == '__main__':
   app.run(host=config_app['host'], port= config_app['port'])

   #test