import csv
import numpy as np

def readCSVs():
    path_arrival_hours = './data/arrival_hours.csv'
    path_charging_volume = './data/charging_volume.csv'
    path_connection_time = './data/connection_time.csv'
    path_solar = './data/solar.csv'
    
    def readPath(path):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            return [castToValue(row) for row in csv_reader]


    return readPath(path_arrival_hours), readPath(path_charging_volume), readPath(path_connection_time), readPath(path_solar)

def castToValue(row):
    if len(row) == 2:
        return [int(row[0]), float(row[1])]
    if len(row) == 3:
        return [int(row[0]), float(row[1]), float(row[2])]


if __name__ == "__main__":
    print(readCSVs())