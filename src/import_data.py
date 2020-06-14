import pandas as pd
import boto3
import logging
import yaml
import os

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config_import_data = config['import_data']

# set up logger
logger = logging.getLogger(__name__)


def importdata(args):
    """Imports the airline data from the public S3 bucket flightdelays9232
    """

    client = boto3.client('s3', aws_access_key_id=args.access_key, aws_secret_access_key= args.secret_key) #low-level functional API
    logging.info("Accessing S3 with access key %s and secret key %s",args.access_key,args.secret_key)


    # Downloads the flight data for every year and month in the list from the public S3 bucket
    obj = client.get_object(Bucket=config_import_data['S3_retrieval_bucket'], Key=config['data_filename'])
    logging.info("Downloaded %s from the %s S3 bucket",config['data_filename'],config_import_data['S3_retrieval_bucket'])
    
    Flights = pd.read_csv(obj['Body']) #temporarily store as Pandas dataframe
    Flights.to_csv(config['data_path']) # saves the flight data in the config data path location
    logging.info("Saved %s at the following location: %s",config['data_filename'],config['data_path'])

    
            