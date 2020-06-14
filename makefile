data/Flights.csv: 
	python move_data.py --access_key ${access_key} --secret_key ${secret_key} --bucket_name ${bucket_name}
data:	data/Flights.csv

sql/FlightDelays.db:
	python create_database.py
localdb:	sql/FlightDelays.db

delay_model.sav: 
	python train_model.py
models:	models/delay_model.sav

# app.py
# 	python app.py
# app:	app.py

all:	data localdb models app


# access_key = default
# secret_key = default
# bucket_name = flightdata4213

# test: venv
# 	. ${project}-env/bin/activate; python run.py test 
# 	. ${project}-env/bin/activate; py.test

# .PHONY: clean-tests clean-env clean-pyc clean app

# clean-tests:
# 	rm -rf .pytest_cache
# 	rm -r test/model/test/
# 	mkdir test/model/test
# 	touch test/model/test/.gitkeep

# clean-env:
# 	rm -r ${project}-env

# clean-pyc:
# 	find . -name '*.pyc' -exec rm -f {} +
# clean: clean-tests clean-env clean-pyc
