import matplotlib.pyplot as plt
import numpy as np
import performanceMeasures

def showParkingDensity(currState):

    parkingPerTimestamp = currState["parkedPerTimestep"]
    maximumParkingAmount = [currState["parkingPlaces"][currID].maxNumberCharginStations for currID in currState["parkingPlaceIDs"] ]
    
    for i in range(7):
        parkingID = str(i + 1)

        xData = [currElement[0] for currElement in parkingPerTimestamp]
        yData = [currElement[1][i] for currElement in parkingPerTimestamp]

        plt.plot(xData, yData)
        plt.axhline(y=maximumParkingAmount[i], color='r', linestyle='-')
        
        plt.title("Parking Density for parking place: " + parkingID)
        plt.show()


def showChargeDensity(currState):

    chargingPerTimestamp = currState["chargingperTimestemp"]
    maximumParkingAmount = [currState["parkingPlaces"][currID].maxNumberCharginStations for currID in currState["parkingPlaceIDs"] ]
    
    for i in range(7):
        parkingID = str(i + 1)

        xData = [currElement[0] for currElement in chargingPerTimestamp]
        yData = [currElement[1][i] for currElement in chargingPerTimestamp]

        plt.plot(xData, yData)
        plt.axhline(y=maximumParkingAmount[i], color='r', linestyle='-')
        plt.title("Charging Density for parking place: " + parkingID)
        plt.show()

def showOverloadDensity(currState):

    chargingPerTimestamp = currState["chargingperTimestemp"]
    powerPerTimestep = currState["powerDrawnPerTimeStep"]

    powerPerCablePerStep = [performanceMeasures.calculateChargePerCable(curr[1]) for curr in powerPerTimestep]

    for cable in powerPerCablePerStep[0].keys():

        xData = [curr[0] for curr in chargingPerTimestamp] 
        yData = [curr[cable] for curr in powerPerCablePerStep]

        plt.plot(xData, yData)
        plt.axhline(y=200, color='r', linestyle='-')
        plt.title("Used capacity for " + cable + ".")
        plt.show()


    xData = [curr[0] for curr in chargingPerTimestamp] 
    yData = [sum(curr[1]) * 6 for curr in chargingPerTimestamp]
    plt.plot(xData, yData)
    plt.axhline(y=1000, color='r', linestyle='-')
    plt.title("Used capacity for the transformer")
    plt.show()

