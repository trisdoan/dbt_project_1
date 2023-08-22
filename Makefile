perms:
	sudo mkdir -p logs plugins temp ./transform/logs ./transform/target ./transform/dbt_modules && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins dags temp ./transform/logs ./transform/target ./transform/dbt_modules

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



####################################################################################################################
# Set up cloud infrastructure
tf-init:
	terraform -chdir=./terraform init

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy

infra-config:
	terraform -chdir=./terraform output

####################################################################################################################
# Port forwarding to local machine

cloud-airflow:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 8080:$$(terraform -chdir=./terraform output -raw ec2_public_dns):8080 && open http://localhost:8080 && rm private_key.pem

cloud-metabase:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 3000:$$(terraform -chdir=./terraform output -raw ec2_public_dns):3001 && open http://localhost:3000 && rm private_key.pem



####################################################################################################################
# Helpers

ssh-ec2:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) && rm private_key.pem