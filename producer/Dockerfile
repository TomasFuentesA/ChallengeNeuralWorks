FROM bitnami/python:3.9

RUN pip install kafka-python
RUN pip install pandas
RUN python -m pip install psycopg2-binary

COPY . .