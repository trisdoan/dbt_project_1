perms:
	mkdir -p logs plugins temp && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins dags temp

docker-up:
	docker compose up airflow-init && docker compose up --build -d

up: perms docker-up
	

down:
	docker compose down --volumes --rmi all --remove-orphans

sh:
	docker exec -ti webserver bash

run-etl:
	docker exec loader python extract_data.py

warehouse:
	docker exec -ti warehouse_db psql postgres://warehouse:warehouse1234@localhost:5433/warehouse_db

customerdb:
	docker exec -ti customer_db psql postgres://customer:customer1234@localhost:5432/customer_db