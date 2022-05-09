import matplotlib.pyplot as plt
import numpy as np

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

    powerPerCablePerStep = [calculateChargePerCable(curr[1]) for curr in powerPerTimestep]

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

def calculateChargePerCable(chargePerTimestep):
    cables = {}
    cables["cable1"] = chargePerTimestep[0]
    cables["cable2"] = chargePerTimestep[1]
    cables["cable3"] = chargePerTimestep[2]
    cables["cable5"] = chargePerTimestep[6]
    cables["cable7"] = chargePerTimestep[4]
    cables["cable8"] = chargePerTimestep[5]
    
    # Compound cables
    cables["cable6"] = cables["cable7"] + cables["cable8"]
    cables["cable4"] = cables["cable6"] + cables["cable5"] + chargePerTimestep[3]
    cables["cable0"] = cables["cable1"] + cables["cable2"] + cables["cable3"]
    

    return cables