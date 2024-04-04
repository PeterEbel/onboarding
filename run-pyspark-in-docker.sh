#!/bin/bash

CONTAINER=$(docker run -d --rm --name my-pyspark -p 8888:8888 -v /home/peter/projects/onboarding:/home/jovyan/work jupyter/pyspark jupyter notebook --ip 0.0.0.0)
docker cp /home/peter/projects/postgres/lib/postgresql-42.7.0.jar $CONTAINER:/usr/local/spark/jars
docker cp /home/peter/projects/iceberg/lib/iceberg-spark-runtime-3.5_2.12-1.4.0.jar $CONTAINER:/usr/local/spark/jars
export CONTAINER
sleep 5
docker exec $CONTAINER jupyter server list
