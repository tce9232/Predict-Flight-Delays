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
import yaml
import os

# import config yaml file
with open("../config/test_model_config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


Base = declarative_base()

class FlightDelays(Base):
    """ Defines the data model for the table `FlightDelays. """

    __tablename__ = 'FlightDelays'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    month = Column(String(100), unique=False, nullable=False)
    weekday = Column(String(100), unique=False, nullable=False)
    airline = Column(String(100), unique=False, nullable=False)
    airport = Column(String(100), unique=False, nullable=False)
    state = Column(String(100), unique=False, nullable=False)
    cancel_pred = Column(String(100), unique=False, nullable=False)
    delay_pred = Column(String(100), unique=False, nullable=False)
    

    def __repr__(self):
        risk_repr = "<FlightDelays(client_id='%s', prediction='%s')>"
        return risk_repr % (self.id, self.prediction)



def create_db(args,engine=None):
    """ Returns the appropriate engine string when connecting to a SQL database"""
    
    if engine is None:
        if args.RDS:
            conn_type = "mysql+pymysql"
            user = os.environ.get("MYSQL_USER")
            password = os.environ.get("MYSQL_PASSWORD")
            host = os.environ.get("MYSQL_HOST")
            port = os.environ.get("MYSQL_PORT")
            DATABASE_NAME = 'msia423'
            engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
            logging.debug("engine string: %s"%engine_string)

        else:
            engine_string = args.local_URI
            logging.debug("engine string: %s"%engine_string)
        
        engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)

    return engine


if __name__ == "__main__":
    # parse user arguments for setting up the database
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default=False, action="store_true", help="True if want to create in RDS else None")
    parser.add_argument("--local_URI", default=config['flight_db_path'])
    args = parser.parse_args()
    
    engine = create_db(args)

    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    # create a set of rows that contain all the possible combinations for predicting flight data
    iterated_preds = makepredictions(make_iterations())

    # add every row to the dataframe
    count = 0
    for row in iterated_preds.itertuples():
        flight_iteration = FlightDelays(month=str(row.MONTH), weekday=str(row.DAY_OF_WEEK), airline=str(row.OP_UNIQUE_CARRIER), airport=str(row.ORIGIN_AIRPORT_ID), state=str(row.DEST_STATE_ABR), cancel_pred=str(row.cancel_pred), delay_pred=str(row.delay_pred))
        session.add(flight_iteration)
        count += 1

        
    logging.info("%s flight iterations added to database session", count)
    session.commit()
    logging.info("Flight iterations committed to database session")

    session.close()
