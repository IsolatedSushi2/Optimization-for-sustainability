
import parkingPlace


def createInitialState():
    state = {}

    state["parkingPlaces"] = parkingPlace.createParkingPlaces()


    return state
