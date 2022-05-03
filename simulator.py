import event
import state
import generator
import logger

def startSimulation(eventQueue):

    eventHandlers = {"carArrives": handleCarArrivalEvent,
                     "solarUpdate": handleSolarUpdateEvent,
                     "carLeaves": handleCarLeavesEvent}

    currState = state.createInitialState()
    while not eventQueue.empty():
        currEvent = eventQueue.get()
        logger.logEvent(currEvent)
        currEventType = currEvent.eventType

        assert currEventType in eventHandlers
        
        returnEvent = eventHandlers[currEventType](currEvent, currState)
        
        if returnEvent is not None:
            eventQueue.put(returnEvent)



def handleCarArrivalEvent(currEvent, currState):
    currCar = currEvent.data
    currCar.carParksVisited.append(currCar.parkingPlaceID)

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    if currParkingPlace.isFull():
        return handleCarPlaceFull(currEvent, currState)
        

    currParkingPlace.arriveAtCharger()
    return event.Event(time=currEvent.time + currCar.connectionTime, eventType="carLeaves", data=currCar)

def handleCarPlaceFull(currEvent, currState):
    currCar = currEvent.data

    if len(currCar.carParksVisited) == 3:
        logger.logMessage("Too many Car Places (3) full in a row")
        return None

    #TODO normal distributed travel time to other parkingPlace
    timeToTravel = 10 * 60
    currCar.parkingPlaceID = generator.generateParkingPlace(currCar.carParksVisited)
    logger.logMessage("Car Place full, moving to another")
    return event.Event(time=currEvent.time + timeToTravel, eventType="carArrives", data=currCar)

def handleCarLeavesEvent(currEvent, currState):
    currCar = currEvent.data

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    currParkingPlace.leaveCharger()


def handleSolarUpdateEvent(currEvent, currState):
    return None
        
