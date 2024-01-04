#!/bin/bash

function up {
    docker volume prune -f
    docker build -t poketcgdata-airflow -f ./Dockerfile ./
    docker-compose -f docker-compose.yaml up --remove-orphans -d
}

function down {
    docker-compose down
}

function restart {
    down
    up
}

${1}