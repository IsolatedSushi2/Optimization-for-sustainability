from constants import CAR_AMOUNT
from dataReader import readCSVs
import generator
from queue import PriorityQueue
from enum import Enum
import eventHandler

class Car():
    parkingPlacesVisited = []

def main():
    arrival_data, charging_volume_data, connection_time_data = readCSVs()

    eventQueue = PriorityQueue()
    events = generator.generateCarArrivalEvents(None, None, None, None, CAR_AMOUNT)

    for currEvent in events:
        eventQueue.put(currEvent)  



    nextTime, eventData = eventQueue.get()
    print(eventData)
    # for event in zip(eventTimes, randomArrivalEvents):
    #     eventQueue.put((randomTime, randomEvent)

    state = {"time": 0}

    # while not eventQueue.empty():
    #     events.eventHandler(eventQueue)



if __name__ == "__main__":
    main()
