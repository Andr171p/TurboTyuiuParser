import psycopg2
from DataBase.PostgreSQL.db_auth_data import host, user, password, db_name, port
from Avito.AvitoParser.utils.preprocessing_data import csv_to_array


def db_connect(file_path):
    data_parser = csv_to_array(
        file_path=file_path
    )
    data_parser = list(filter(any, data_parser))

    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO komerc (information, price, area, address, datas, url, id_, category_id, photo) VALUES (%s, %s, %s, %s, %s, %s)"
            for row in data_parser:
                cursor.execute(sql, row)
    except Exception as _ex:
        print("[INFO] Error while working with PostgresSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("[INFO] PostgresSQL connection closed")


db_connect(
    file_path=r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\Data\ads.csv"
)