## How to run Jupyter Notebook and PySpark in Docker ##


### Install Docker ###

Install Docker following the instructions for your operating system.

### Download the jupyter/pyspark-notebook image

Once installed download the jupyter/pyspark-notebook image.
```
docker pull jupyter/pyspark-notebook
```


### Create a bash file ###

Create a bash file (e.g. run.sh) with the following content:

```
#!/bin/bash

CONTAINER=$(docker run -d --rm --name my-pyspark -p 8888:8888 -v /home/peter/projects:/home/jovyan/work jupyter/pyspark-notebook)
docker cp /home/peter/projects/postgres/lib/postgresql-42.7.0.jar $CONTAINER:/usr/local/spark/jars
docker cp /home/peter/projects/iceberg/lib/iceberg-spark-runtime-3.5_2.12-1.4.0.jar $CONTAINER:/usr/local/spark/jars
export CONTAINER
sleep 5
docker exec $CONTAINER jupyter server list
```

For Windows, create a corresponding Powershell file and adapt the syntax join above. 

The second line creates a container (with the name "my-pyspark") from the downloaded image, maps the Juypter port 8888 so it becomes accessible outside the container under the same port number, and additionally maps the pre-configured home directory inside the container (/home/jovyan/work) to a folder in the file system of your operating system (here: /home/peter/projects). Any filed stored there will appear later inside the container as if it were local. The third and fourth line show how to copy libraries like database drivers into Sparks library folder inside the container (e.g. to read from a Postgres database within your Spark program).

### Open the Jupyter Notebook in your browser ###

Open your preferred browser and enter the following as URL:

```
localhost:8888/tree?token=0f9541f307a73fcd220474bfd24d2476ea145d58d165ad1b
```
The token (here: 0f9541f307a73fcd220474bfd24d2476ea145d58d165ad1b) will be different each time you start Jupyter Notebook. The token you need for the current Juypter session is shown on the screen when the run script terminates. Look for "token=".

```
Currently running servers:
http://cc03a1a1513f:8888/?token=2ea951ec0dc87115a4f40a7b21f1a7b823ce3379a14f94fb
```

## How to run Jupyter Notebook and PySpark in Anaconda ##

### Install Anaconda or Minoconda ###

Install Anaconda or Miniconda following the instructions for your operating system.

### Create a virtual environment ###

Create a file env.yml with the following content in your working directory. Replace the name "Onboarding" with the name of your project.

```
name: onboarding
channels:
  - conda-forge
dependencies:
  - python=3.10
  - pyspark=3.5
  - pypandoc=1.12
  - pytest=7.4.3
  - pylint=3.0.3
  - findspark=2.0.1
  - jupyter=1.0.0
  - pandas=2.2.1
  - numpy=1.26.4
  - openpyxl=3.1.2
  ```
  Then run

  ```
  conda env create -f env.yml
  ```

Conda will download all the required packages and take care of all dependencies. This may take a couple minutes. Once ready activate the new environment with

```
conda activate onboarding
```

To start Jupyter Notebook enter

```
jupyter notebook
```





