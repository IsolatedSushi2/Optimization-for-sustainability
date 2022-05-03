
import parkingPlace

#Create the initial state with some variables
def createInitialState():
    state = {}

    state["parkingPlaces"] = parkingPlace.createParkingPlaces()
    state["carsCharged"] = 0
    state["carsUnableCharged"] = 0
    state["carsAtFullParking"] = 0

    return state

#Print the results after the simulation
def printResults(currState):
    print(currState["carsCharged"], "cars were charged")
    print(currState["carsUnableCharged"], "cars were unable to be charged")
    print(currState["carsAtFullParking"], "times cars arrived at a full parking place")