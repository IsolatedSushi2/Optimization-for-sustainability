
import parkingPlace

#Create the initial state with some variables
def createInitialState(chargingStrategy = 'base'):
    state = {}
    state["parkingPlaceIDs"] = ["1", "2", "3", "4", "5", "6", "7"]
    state["parkingPlaces"] = parkingPlace.createParkingPlaces()
    state["carsCharged"] = 0
    state["carsUnableCharged"] = 0
    state["carsAtFullParking"] = 0
    state["chargingStrategy"] = chargingStrategy #This should be 'base', 'price-driven', 'FCFS' or 'ELFS'
    return state

# Clear the files in order to use them for this simulation
def clearPerformanceFiles():
    file = open('./performances/parkingDensity.txt',"w")
    file.close()

    file = open('./performances/chargingDensity.txt',"w")
    file.close()

    file = open('./performances/powerDensity.txt',"w")
    file.close()


# Store the data for the timesteps
def storeDataPerTimestep(currTimestamp, state):

    parkingIDS = state["parkingPlaceIDs"]
    allcurrentlyParked = [len(state["parkingPlaces"][currID].currentlyParked) for currID in parkingIDS]
    allcurrentlyCharging = [len(state["parkingPlaces"][currID].currentlyCharging) for currID in parkingIDS]
    allPowerDrawn = [max(0,len(state["parkingPlaces"][currID].currentlyCharging) * 6 - state["parkingPlaces"][currID].currSolarEnergy) for currID in parkingIDS]

    #Append the data to files
    with open('./performances/parkingDensity.txt', "a") as myfile:     
        myfile.write(str(currTimestamp) + "," + ",".join(map(str,allcurrentlyParked)) + "\n")

    with open('./performances/chargingDensity.txt', "a") as myfile:     
        myfile.write(str(currTimestamp) + "," + ",".join(map(str,allcurrentlyCharging)) + "\n")

    with open('./performances/powerDensity.txt', "a") as myfile:     
        myfile.write(str(currTimestamp) + "," + ",".join(map(str,allPowerDrawn)) + "\n")

#Print the results after the simulation
def printResults(currState):
    print(currState["carsCharged"], "cars were charged")
    print(currState["carsUnableCharged"], "cars were unable to be charged")
    print(currState["carsAtFullParking"], "times cars arrived at a full parking place")