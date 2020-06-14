import pickle 
import pandas as pd
import logging
import yaml
import os

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config_make_predictions = config['make_predictions']

# set up the logger
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def makepredictions(data):
    """ 
    Loads the delay and cancel regression models and uses them to make predictions on the flights data
  
    Parameters: 
    data (df): Flights dataframe to predict from 
  
    Returns: 
    data: Flights dataframe with predictions appended
  
    """

    # loads delay and cancel regression models from their source
    delayreg = pickle.load(open(config['path_to_delay_model'], 'rb'))
    logging.info("Flight delay model loaded from %s", config['path_to_delay_model'])
    
    cancelreg = pickle.load(open(config['path_to_cancel_model'], 'rb'))
    logging.info("Flight cancelation model loaded from %s", config['path_to_cancel_model'])

    # makes predictions from the models based off of the input dataframe
    data['delay_pred'] = delayreg.predict(data[['MONTH','DAY_OF_WEEK','OP_UNIQUE_CARRIER','ORIGIN_AIRPORT_ID','DEST_STATE_ABR']])

    data['cancel_pred'] = cancelreg.predict(data[['MONTH','DAY_OF_WEEK','OP_UNIQUE_CARRIER','ORIGIN_AIRPORT_ID','DEST_STATE_ABR']])

    # saves the dataframe with predictions in the prediction path
    data.to_csv(config_make_predictions['predictions_path'])
    logging.info("Predictions saved to %s", config_make_predictions['predictions_path'])
    return data


def make_iterations():
    """
    Creates every possible iteration of the flights dataframe
    """

    # read in flights data from the data path
    data = pd.read_csv(config['data_path'])
    logging.info("Dataframe loaded from %s", config['data_path'])

    # find all unique values for the variables
    list = []
    month = data['MONTH'].unique()
    weekday = data['DAY_OF_WEEK'].unique()
    airline = data['OP_UNIQUE_CARRIER'].unique()
    airport = data['ORIGIN_AIRPORT_ID'].unique()
    state = data['DEST_STATE_ABR'].unique()

    # iterate through the unique values to create all possible input values for the model
    for m in month:
        for w in weekday:
            for l in airline:
                for p in airport:
                    for s in state:
                        list.append([m,w,l,p,s])


    # return every possible iteration as a dataframe
    new = pd.DataFrame(list)
    new.columns = ['MONTH','DAY_OF_WEEK','OP_UNIQUE_CARRIER','ORIGIN_AIRPORT_ID','DEST_STATE_ABR']
    logging.info("iteration list created")
    return new

if __name__ == '__main__':

    makepredictions()
