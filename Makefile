perms:
	mkdir -p logs plugins temp ./transform/logs ./transform/target ./transform/dbt_modules && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins dags temp ./transform/logs ./transform/target ./transform/dbt_modules

docker-up:
	docker compose up airflow-init && docker compose up --build -d

up: perms docker-up
	

down:
	docker compose down --volumes --rmi all --remove-orphans && sudo rm -rf logs plugins temp  ./transform/logs ./transform/target  ./transform/dbt_modules

sh:
	docker exec -ti webserver bash

# run-etl:
# 	docker exec loader python extract_data.py

warehouse:
	docker exec -ti warehouse_db psql postgres://warehouse:warehouse1234@localhost:5432/warehouse_db

customerdb:
	docker exec -ti customer_db psql postgres://customer:customer1234@localhost:5432/customer_db

viz:
	open http://localhost:3000


#######FORMAT CODE########
format:
	docker exec formatter python -m black -S --line-length 79 .

isort:
	docker exec formatter isort .

sql-format:
	docker exec formatter sql-formatter /code/transform/models/*.sql

lint: 
	docker exec formatter flake8 /code/dags

format-code: isort format sql-format lint