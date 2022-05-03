from constants import CAR_AMOUNT
from dataReader import readCSVs
from generator import generateCarArrivals
from queue import PriorityQueue
from enum import Enum
import eventHandler

class Car():
    parkingPlacesVisited = []

def main():
    eventQueue = PriorityQueue()
    state = {"time" = 0,
             "parkingPlacesVisited" = 0, # 
             ""}

    while not eventQueue.empty():
        events.eventHandler(eventQueue)

    arrival_data, charging_volume_data, connection_time_data = readCSVs()
    #generateCarArrivals(arrival_data, CAR_AMOUNT)


if __name__ == "__main__":
    main()
