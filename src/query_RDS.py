import os
import sys
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
import logging.config
import argparse
import logging
import pandas as pd
from make_predictions import *
from create_database import *
import yaml
import os

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config_query_RDS = config['query_RDS']

# set up logger
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def queryRDS(month, weekday, airline, airport, state):
    """ 
    queries flights database
  
    Given input variables, this queries the flights database that was setup locally or on RDS and returns the predicted values
  
    Parameters: 
    month (str): month of the flight
    weekday (str): weekday of the flight 1-7 with 1 being a monday
    airline (str): airline code of the flight
    airport (str): airport code of the flight
    state (str): state the flight is departing towards
  
    Returns: 
    df: Dataframe with formatted cancel and delay predictions for the given flight
  
    """
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default=False, action="store_true", help="True if want to create in RDS else None")
    parser.add_argument("--local_URI", default=config['flight_db_path'])

    args = parser.parse_args()
    
    engine = create_db(args)

    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    #query table for row with given inputs
    query = "SELECT cancel_pred, delay_pred FROM FlightDelays WHERE month = " + str(month) + " AND weekday = " + str(weekday) + " AND airline = \'" + str(airline) + "\' AND airport = " + str(airport) + " AND state = \'" + str(state) + "\'"
    df = pd.read_sql(query, con=engine)
    logging.info('Dataframe queried and returned with size of %s', df.shape)

    # convert the cancel and delay predictions to the appropriate output
    df['cancel_pred'] = pd.to_numeric(df['cancel_pred']).round(4)*100
    df['delay_pred'] = pd.to_numeric(df['delay_pred']).round(1)
    
    session.close()

    return df



