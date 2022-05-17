import matplotlib.pyplot as plt
import numpy as np
import performanceMeasures


def showPlots(currState):
    showParkingDensity(currState)
    showChargeDensity(currState)
    showOverloadDensity(currState)


def readFile(path):

    timestamps = []
    dataPoints = []
    with open(path, "r") as file:
        lines = file.readlines()

        for line in lines:
            tokens = line.split(',')
            tokens = [float(curr) for curr in tokens]
            timestamps.append(tokens[0])
            dataPoints.append(tokens[1:])

    return timestamps, dataPoints

def showParkingDensity(currState):

    timestamps, data = readFile('./performances/parkingDensity.txt')
    maximumParkingAmount = [currState["parkingPlaces"][currID].maxNumberCharginStations for currID in currState["parkingPlaceIDs"] ]
    
    for i in range(7):
        parkingID = str(i + 1)

        xData = timestamps
        yData = [dataPoint[i] for dataPoint in data]

        plt.plot(xData, yData)
        plt.axhline(y=maximumParkingAmount[i], color='r', linestyle='-')
        
        plt.title("Parking Density for parking place: " + parkingID)
        plt.show()


def showChargeDensity(currState):

    timestamps, data = readFile('./performances/chargingDensity.txt')
    maximumParkingAmount = [currState["parkingPlaces"][currID].maxNumberCharginStations for currID in currState["parkingPlaceIDs"] ]
    
    for i in range(7):
        parkingID = str(i + 1)

        xData = timestamps
        yData = [dataPoint[i] for dataPoint in data]

        plt.plot(xData, yData)
        plt.axhline(y=maximumParkingAmount[i], color='r', linestyle='-')
        plt.title("Charging Density for parking place: " + parkingID)
        plt.show()

def showOverloadDensity(currState):

    timestamps, data = readFile('./performances/powerDensity.txt')

    powerPerCablePerStep = [performanceMeasures.calculateChargePerCable(curr) for curr in data]

    for cable in powerPerCablePerStep[0].keys():

        xData = timestamps
        yData = [curr[cable] for curr in powerPerCablePerStep]

        plt.plot(xData, yData)
        plt.axhline(y=200, color='r', linestyle='-')
        plt.title("Used capacity for " + cable + ".")
        plt.show()


    xData = timestamps
    yData = [sum(curr) for curr in data]
    plt.plot(xData, yData)
    plt.axhline(y=1000, color='r', linestyle='-')
    plt.title("Used capacity for the transformer")
    plt.show()

