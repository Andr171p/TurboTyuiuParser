import pandas as pd
import csv


def replace_symbol(string):
    TOKEN_SYMBOLS = ["\n", "\xa0"]
    for symbol in TOKEN_SYMBOLS:
        string = string.replace(symbol, "")

    return string


def drop_none(data):
    print(len(data))
    dataframe = pd.DataFrame(data)
    dataframe = dataframe.dropna()
    return dataframe.values.tolist()


def save_to_csv(data, file_path):
    with open(file_path, "w", encoding="windows-1251") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        for i in data:
            csv_writer.writerow(i)


def csv_to_array(file_path):
    array = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            array.append(row)
    return array

