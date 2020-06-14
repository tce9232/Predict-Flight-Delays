from sklearn import linear_model
import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
import pickle
import logging
import yaml
import os
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statistics

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# set up logger
logging.basicConfig(level=logging.INFO)


def trainmodel():
    """
    Trains a cancel and delay model using data from the data_path in the config file and outputs a cancel and delay model
    """

    # import data from data path
    data = pd.read_csv(config['data_path'])
    logging.info('Data loaded from %s', config['data_path'])

    lm = linear_model.LinearRegression()

    # create testing and training splits in the delay dataset
    dfDelay = generate_delay_features(data)
    delay_X_train = dfDelay['delay_X_train']
    delay_Y_train = dfDelay['delay_Y_train']
    delay_X_test = dfDelay['delay_X_test']
    delay_Y_test = dfDelay['delay_Y_test']
    delay_train = pd.concat([delay_Y_train,delay_X_train],axis=1,sort=False)

    # create testing and training splits in the cancel dataset
    dfCancel = generate_cancel_features(data)
    cancel_X_train = dfCancel['cancel_X_train']
    cancel_Y_train = dfCancel['cancel_Y_train']
    cancel_X_test = dfCancel['cancel_X_test']
    cancel_Y_test = dfCancel['cancel_Y_test']
    cancel_train = pd.concat([cancel_Y_train,cancel_X_train],axis=1,sort=False)

    # fit the delay model
    delaymod = smf.ols(formula='ARR_DELAY ~ MONTH + DAY_OF_WEEK + OP_UNIQUE_CARRIER + ORIGIN_AIRPORT_ID + DEST_STATE_ABR', data=delay_train)
    delayreg = delaymod.fit()

    # create and save the metrics and summary of flight delay model
    delay_results = []
    delay_residuals = abs(delay_Y_test - delayreg.predict(delay_X_test))
    delay_results.append("average delay resid: " + str(np.nanmean(delay_residuals)))
    delay_results.append("median delay resid: " + str(statistics.median(delay_residuals)))
    delay_results = pd.DataFrame(delay_results)
    delay_results.to_csv("delay_model_metrics")
    with open('delay_summary.txt', 'w') as fh:
        fh.write(delayreg.summary().as_text())
    
    # fit the cancel model
    cancelmod = smf.logit(formula='CANCELLED ~ MONTH + DAY_OF_WEEK + OP_UNIQUE_CARRIER + ORIGIN_AIRPORT_ID + DEST_STATE_ABR', data=cancel_train)
    cancelreg = cancelmod.fit()

    # create and save the summary of the flight cancel model
    with open('cancel_summary.txt', 'w') as fh:
        fh.write(cancelreg.summary().as_text())

    # save the delay and cancel models
    pickle.dump(delayreg, open('delay_model.sav', 'wb'))
    logging.info('Delay model saved')
    pickle.dump(cancelreg, open('cancel_model.sav', 'wb'))
    logging.info('Cancel model saved')

def generate_delay_features(data):
    """
    Generates a dataframe to use for the delay model

    Parameters: 
    data (df): the flights dataframe
  
    Returns: 
    delay_dict: a dictionary of testing and training splits for both predictive and response variables
    """

    try:
        # define x and y features
        X = data[['MONTH','DAY_OF_WEEK','OP_UNIQUE_CARRIER','ORIGIN_AIRPORT_ID','DEST_STATE_ABR']]
        Y = data['ARR_DELAY']
        # create the training and testing splits for the data
        delay_X_train, delay_X_test, delay_Y_train, delay_Y_test = train_test_split(X, Y, test_size=config['test_split'], random_state=320)
        delay_dict = dict()
        delay_dict['delay_X_train'] = delay_X_train
        delay_dict['delay_X_test'] = delay_X_test
        delay_dict['delay_Y_train'] = delay_Y_train
        delay_dict['delay_Y_test'] = delay_Y_test
        return delay_dict

    except KeyError:
        logging.warning('generate_delay_features did not find all the necessary columns in the dataset to build the model')
        raise

 
def generate_cancel_features(data):
    """
    Generates a dataframe to use for the cancel model

    Parameters: 
    data (df): the flights dataframe
  
    Returns: 
    cancel_dict: a dictionary of testing and training splits for both predictive and response variables
    """

    try:
        # define x and y features
        X = data[['MONTH','DAY_OF_WEEK','OP_UNIQUE_CARRIER','ORIGIN_AIRPORT_ID','DEST_STATE_ABR']]
        Y = data['CANCELLED']
        # create the training and testing splits for the data
        cancel_X_train, cancel_X_test, cancel_Y_train, cancel_Y_test = train_test_split(X, Y, test_size=config['test_split'], random_state=1)
        cancel_dict = dict()
        cancel_dict['cancel_X_train'] = cancel_X_train
        cancel_dict['cancel_X_test'] = cancel_X_test
        cancel_dict['cancel_Y_train'] = cancel_Y_train
        cancel_dict['cancel_Y_test'] = cancel_Y_test
        return cancel_dict

    except KeyError:
        logging.warning('generate_delay_features did not find all the necessary columns in the dataset to build the model')
        raise

    
if __name__ == '__main__':

    
    trainmodel()

