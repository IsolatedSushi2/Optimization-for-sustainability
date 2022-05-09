
import parkingPlace

#Create the initial state with some variables
def createInitialState():
    state = {}
    state["parkingPlaceIDs"] = ["1", "2", "3", "4", "5", "6", "7"]
    state["parkingPlaces"] = parkingPlace.createParkingPlaces()
    state["carsCharged"] = 0
    state["carsUnableCharged"] = 0
    state["carsAtFullParking"] = 0
    state["parkedPerTimestep"] = []
    state["chargingperTimestemp"] = []
    state["powerDrawnPerTimeStep"] = []

    return state

def storeDataPerTimestep(currTimestamp, state):

    parkingIDS = state["parkingPlaceIDs"]
    allcurrentlyParked = [state["parkingPlaces"][currID].amountCurrentlyParked for currID in parkingIDS]
    allcurrentlyCharging = [state["parkingPlaces"][currID].amountCurrentlyCharging for currID in parkingIDS]
    allPowerDrawn = [max(0,state["parkingPlaces"][currID].amountCurrentlyCharging * 6 - state["parkingPlaces"][currID].currSolarEnergy) for currID in parkingIDS]

    state["parkedPerTimestep"].append((currTimestamp, allcurrentlyParked))
    state["chargingperTimestemp"].append((currTimestamp, allcurrentlyCharging))
    state["powerDrawnPerTimeStep"].append((currTimestamp, allPowerDrawn))

#Print the results after the simulation
def printResults(currState):
    print(currState["carsCharged"], "cars were charged")
    print(currState["carsUnableCharged"], "cars were unable to be charged")
    print(currState["carsAtFullParking"], "times cars arrived at a full parking place")



# def storeResults(currState):
#     with open('./results', 'w') as f:
#         for item in my_list:
#             f.write("%s\n" % item)