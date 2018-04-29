
init:
	sudo apt-get install -y build-essential python-dev python-pip
	source partial-api/env3/bin/activate
	sudo pip install -r partial-api/requirements.txt

activate:
	virtualenv -p python3 partial-api/env3
	source partial-api/env3/bin/activate
	sudo pip install -r partial-api/requirements.txt

start: init
	gunicorn -w 4 -b 0.0.0.0:4000 api:app

test:
	py.test --verbose tests/

cvg:
	py.test --verbose --cov-report term --cov=countries tests/

ci: init
	py.test tests/ --junitxml=junit-results.xml

db:
	docker-compose up database &
	docker ps
	echo "Container OK"

psql:
	docker run -d \
	--name postgres \
	-p 5433:5432 \
	-e POSTGRES_PASSWORD="pass" \
	postgres

cp-files:
	python3 data/parse.py
	sleep 2
	docker cp $(shell pwd)/data/schema.sql postgres:/
	docker cp $(shell pwd)/data/currencies.sql postgres:/
	docker cp $(shell pwd)/data/countries.sql postgres:/
	docker cp $(shell pwd)/data/load.sh postgres:/

load-data:
	sleep 3
	docker exec --user postgres postgres sh /load.sh


deploy:
	eval $(docker-machine env partial-docker-v1-2gb)