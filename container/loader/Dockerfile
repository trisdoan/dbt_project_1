FROM python:3.7-slim

# set up location of code
WORKDIR /opt/dbt_project_1/src

# lets us import from folders inside /src/loader directly
ENV PYTHONPATH=/opt/dbt_project_1

# install python requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY our code folder to docker
COPY ../.. /opt/dbt_project_1

# keep our docker container running
CMD ["tail", "-f", "/dev/null"]
