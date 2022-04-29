import csv
import numpy as np

def readCSVs():
    with open('./data/arrival_hours.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        arrival_data = [castToValue(row) for row in csv_reader]

    with open('./data/charging_volume.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        charging_volume_data = [castToValue(row) for row in csv_reader]

    with open('./data/connection_time.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        connection_time_data = [castToValue(row) for row in csv_reader]

    return np.array(arrival_data), np.array(charging_volume_data), np.array(connection_time_data)

def castToValue(row):
    return [int(row[0]), float(row[1])]


if __name__ == "__main__":
    print(readCSVs())