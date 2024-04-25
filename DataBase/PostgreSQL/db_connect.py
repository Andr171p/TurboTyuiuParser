import psycopg2
from DataBase.PostgreSQL.db_auth_data import host, user, password, db_name, port


def db_connect(data_parser):
    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )