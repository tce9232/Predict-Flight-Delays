import pandas as pd
import boto3
import sys
from boto3.session import Session
sys.path.append('..')
import config
import logging
import yaml
import os

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config_upload_data = config['upload_data']

# set up logger
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def uploaddata(args):

    """Uploads airline data to private S3 bucket

    Args:
        bucketname: The private bucket name in which you'd like to store the airline data
    """

    # Upload the flight data for every year and month in the list to the private S3 bucket
    session = Session(aws_access_key_id=args.access_key, aws_secret_access_key=args.secret_key, region_name = args.region_name)
    s3 = session.resource('s3', region_name=config_upload_data['S3_region_name'])
    s3.meta.client.upload_file(config['data_path'], args.bucket_name,config['data_filename'])
    logging.info("Uploaded %s from %s filepath to the %s S3 bucket", config['data_filename'], config['data_path'], args.bucket_name)