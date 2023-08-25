FROM bitnami/python:3.9

RUN python3 -m pip install psycopg2-binary
RUN python3 -m pip install pandas
RUN python3 -m pip install numpy
RUN python3 -m pip install seaborn
RUN python3 -m pip install -U scikit-learn

COPY . .