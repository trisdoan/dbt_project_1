FROM python:3.7-slim

RUN pip install \
    psycopg2-binary==2.9.3 \
    faker==13.3.2 \
    boto3==1.21.21

WORKDIR /opt/datagenerator

COPY ../../datagenerator /opt/datagenerator

CMD [ "python" "./generate_fake_data.py"]