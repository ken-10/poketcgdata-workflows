####################################################################################################################
# Setup containers to run Airflow

docker-build:
	docker build -t poketcgdata-airflow -f ./Dockerfile ./

dc-up: 
	docker compose -f docker-compose.yaml up --remove-orphans -d

perms: 
	sudo mkdir -p ./logs ./plugins ./config && sudo chmod -R u=rwx,g=rwx,o=rwx ./logs ./plugins ./config ./dags ./tests

up: perms docker-build dc-up

down: 
	docker compose down

sh: 
	docker exec -ti webserver bash

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
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 8081:$$(terraform -chdir=./terraform output -raw ec2_public_dns):8080 && open http://localhost:8081 && rm private_key.pem

####################################################################################################################
# Helpers

ssh-ec2:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) && rm private_key.pem
