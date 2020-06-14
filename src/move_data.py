from import_data import *
from upload_data import *
import argparse

parser = argparse.ArgumentParser(description="Uploading data to S3")

parser.add_argument("--access_key", help="AWS access key")
parser.add_argument("--secret_key", help="AWS secret access keye")
parser.add_argument("--bucket_name",help="S3 bucket name")
parser.add_argument("--region_name",default='us-east-2', help="S3 bucket region name")

args = parser.parse_args()

#Takes airline data from public S3 bucket and moves it to specified private S3 bucket
importdata(args)
uploaddata(args)