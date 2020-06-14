access_key = default
secret_key = default
bucket_name = flightdata4213

../data/Flights.csv:	move_data.py	import_data.py	upload_data.py
	python move_data.py --access_key ${access_key} --secret_key ${secret_key} --bucket_name ${bucket_name}
data:	../data/Flights.csv

sql/FlightDelays.db:	create_database.py
	python create_database.py
localdb:	sql/FlightDelays.db

../models/delay_model.sav:	../models/train_model.py
	cd ..;	cd models;	python train_model.py
models:	../models/delay_model.sav

.PHONY:	../app/app.py
../app/app.py:
	cd ..;	cd app;	python app.py
app:	../app/app.py

all:	data localdb models app

.PHONY:	../test/test_train_model.py
../test/test_train_model.py:
	cd ..;	cd test;	pytest
test:	../test/test_train_model.py
