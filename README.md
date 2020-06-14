# Example project repository
 
<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Move Data to your S3 Bucket](#3-move-data-to-your-S3-bucket)
  * [4. Train the model](#4-train-the-model)
  * [5. Initialize the database](#4-initialize-the-database)
  * [6. Run the application](#4-run-the-application)
  * [7. Testing](#7-testing)
  * [8. Using the makefile](#8-using-the-makefile)

<!-- tocstop -->


## Project Charter

  

****Vision****: To enable people to make educated decisions around the likelihood and extent to which their flights will be delayed. Air travel is becoming increasingly accessible to people in the United States, with one third of people in the U.S. having flown in the last year. This places a greater importance on the reliability of this transportation. Flight cancelations or delays can range from a small nuisance to a major problem for travelers. Airlines offer no easy way to check the history of delays for a particular route or time. This tool would provide that information for the consumer.
 

****Mission****: Enable users to input their basic flight information, and report back a percentage chance the flight will be cancelled or delayed, and if delayed, how long. Distinguishing between cancellations and delays is important for this tool because it greatly affects a consumer would make when deciding between tickets. Delays are an annoyance, but cancelations can completely ruin a trip. We will accomplish this by modeling data taken from the Bureau of Transportation Statistics for domestic flights in the US in 2018. 

   

****Success criteria****: We will consider the project successful if the model predicts delays with a misclassification rate of less than 25% and predicts length of delay on average within 10 minutes of the actual result.
Additionally, we would consider the business outcome a success if more than 50% of users reuse this application for a different flight on a later date.

  

## Backlog

## Planning
### Data Gathering - (Retrieve the data necessary for the web app)

 - #### Pull Data From Website - (download necessary data)
	 - Download a year worth of data files
	 - Append data to one another
	 - Upload into Python
- #### Exploratory Data Analysis - (validate data)
	 - Check data for missing values or outliers
	 - Check for any multicollinearity in the data I'll be using - Look for any additional factors for possible inclusion into the model


### Data Modeling - (Create models for predicting delays and cancellations)

 - #### Data Cleaning - (Format the data so it's ready for oeling) - ####Data eing
	 - Reformat any columns as necessary
	 - Merge necessary information
 
 - #### Feature Engineering - (Create new factors)
	 - Calculate new columns necessary for the app

- #### Model Building - (Create and determine the best model to use in the web app)
	 - Run basic linear model for cancellation detection
	 - Run basic linear model for delay time
	 - Look at more complex models for cancellation detection
	 - Look at more complex models for delay time
	 - Compare misclassification rates, and pick the best cancellation detection model
	 - Compare delay time models and select the best one

### Building the Web App - (Create and optimize the web app)

- #### Upload Model to AWS

 - #### Build the Web App
	 - Build an interface to allow people to input their flight information
	 - Make App output delay probability


## Backlog
Data Gathering - Pull Data from Website - Download a year worth of data files (1)

Data Gathering - Pull Data from Website - Append data to one another (1)

Data Gathering - Pull Data from Website - Upload into Python (1) 

Data Gathering - Exploratory Data Analysis - Check data for missing values or outliers (1) 

 Gathering - Exploratory Data Analysis - Check for any multicollinearity in the data I'll be using (1) 

Data Gathering - Exploratory Data Analysis - Look for any additional factors for possible inclusion into the model (1) 

Data Modeling - Data Cleaning - Reformat any columns as necessary (1)

Data Modeling - Data Cleaning - Merge necessary information (1)

Data Modeling - Feature Engineering - Calculate new columns necessary for the app (2)

Data Modeling - Model Building - Run basic linear model for cancellation detection (1)

Data Modeling - Model Building - Look at more complex models for cancellation detection (2)

Data Modeling - Model Building - Run basic linear model for delay time prediction (1)

Data Modeling - Model Building - Look at more complex models for delay time prediction (2)

Data Modeling - Model Building - Compare misclassification rates, and pick the best cancellation detection modelone (1)

Data Modeling - Model Building - Compare delay time models, and pick the best one (1)

Building Web App - Build the Web App - Build an interface to allow people to input their flight information (8)

Building Web App - Build the Web App - Make App output delay/cancellation probability, predict delay time (8)

## Icebox
Building Web App - Upload Model to AWS

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv flightdelays

source flightdelays/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n flightdelays python=3.7
conda activate flightdelays
git clone "https://github.com/tce9232/MSiA423-example-project-repo-2019"
pip install -r requirements.txt

```

### 2. Configure Flask app 

`test_model_config.yaml` in the 'config' folder holds the configurations for the Flask app. It includes the following configurations:

```python
HOST = 127.0.0.1 # What host to use for the Flask app
PORT = 3000  # What port to expose app on 
```

If you'd like the app to run on a different host or port, change that number here and save this file before continuing.

### 3. Move Data to your S3 Bucket

In order to move the flight delay data to your own personal S3 bucket, you first need to cd into the src folder:

```python
cd src
```

Then run move_data.py while specifying your AWS access key, AWS security key and personal S3 bucket name you'd like to store the flight data in

```python
python movedata.py --access_key "AWS_access_key" --secret_key "AWS_secret_access_key" --bucket_name "S3_bucket_name"
```

This copies the data from the public flightdelays9232 bucket to the data folder included in this project, then uploads it back to the S3 bucket specified.

### 4. Train the model 

This git repo comes with a pretrained model, but if you'd like to rerun this, you can do so by navigating to the "models" folder and running:

```python
python train_model.py
```

This will train a linear regression model for the flight delay times and logistic regression model for the cancellation indicator. If you'd like to see the output for these models, it's saved as "delay_summary.txt" and "cancel_summary.txt" in the "models" folder. 

In addition to the summaries, the the average and median residual for the delayed time prediction is saved as "delay_model_metrics" in the same folder.

The models themselves are also pickled and stored in the models folder.

### 5. Initialize the database 

To create the database for the flight delays, navigate back to the src folder and run the create_database.py script. 

By default, the script will create a database locally and store it in the sql folder. If you'd like to upload the database to RDS instead, use the RDS option when running the script like so:

```python
python create_database.py --RDS 
```

### 6. Run the application

Now in order to run the application, navigate to the app folder and run the app.py script like so:

```python
python app.py
```

This will launch the app locally at the host and port you specified in the configuration file.


### 7. Testing

Now in order to run the application, navigate to the app folder and run the app.py script like so:

```python
python app.py
```

This will launch the app locally at the host and port you specified in the configuration file.


### 8. Using the makefile

The makefile allows the user to run all of the steps 3-7 without the need to navigate between folders or unecessarily recreate files that are already up to date. Simply navigate to the src folder and...

Use:
    -make data
        -to import the data from the public s3 bucket and reupload to your specified bucket. In order to use this option, you must specify your access_key, secret_key and bucket_name like so:
            "make data access_key=youraccesskey secret_key=yoursecretkey bucket_name=yourbucketname"
    -make localdb
        -to create the local version of the flights database on sqlite 
    -make models
        -to rerun and save the delay and cancelled flights models
    -make app
        -to run the app on the local server using the host and port numbers you input in the test_model_config.yaml
    -make all
        -to run all of the above
    -make tests
        -to run the pytests for the train_model and make_predictions python scripts




