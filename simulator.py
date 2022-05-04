import event
import state
import generator
import logger
import showPlots
import time

# Start the simulation
def startSimulation(eventQueue):

    # The eventhandlers allow the events to be mapped to their handlers
    eventHandlers = {"carArrives": handleCarArrivalEvent,
                     "solarUpdate": handleSolarUpdateEvent,
                     "carLeaves": handleCarLeavesEvent,
                     "carBeginsCharging": handleCarBeginsChargingEvent,
                     "carStopsCharging": handleCarStopsChargingEvent,
                     "carPlannedLeave": handleCarPlannedLeaves}

    currState = state.createInitialState()

    # The event loop
    startTime = time.time()
    while not eventQueue.empty():

        # Get next event and type
        currEvent = eventQueue.get()
        currEventType = currEvent.eventType

        assert currEventType in eventHandlers

        # Some events may schedule new events, schedule those here
        returnEvents = eventHandlers[currEventType](currEvent, currState)
        for returnEvent in returnEvents:
            eventQueue.put(returnEvent)

        # Log every event for debugging
        state.storeDataPerTimestep(currEvent.time, currState)
        logger.logEvent(currEvent)

    print("Simulation took", time.time() - startTime, "seconds")
    state.printResults(currState)
    showPlots.showOverloadDensity(currState)


def handleCarPlannedLeaves(currEvent, currState):
    currCar = currEvent.data

    # Hasnt even started charging, so reuse the connection time
    if currCar.amountCharged == 0 and currCar.chargingVolume > 0:
        return [event.Event(time=currEvent.time + currCar.connectionTime, eventType="carPlannedLeave", data=currCar)]
    # Is finished charging
    elif currCar.amountCharged >= currCar.chargingVolume:
        logger.logMessage(f'Car {currCar.carID}, succesfully charged')
        return [event.Event(time=currEvent.time, eventType="carLeaves", data=currCar)]
    # Hasn't finished charging, but is busy charging
    else:
        logger.logMessage(
            f'Car {currCar.carID}, not succesfully charged. ERROR in basecase')
        currCar.amountCharged = (
            6/3600) * (currEvent.time - currCar.timeStartCharging)
        return [event.Event(time=currEvent.time + (currCar.chargingVolume - currCar.amountCharged) / (6/3600), eventType="carLeaves", data=currCar)]


def handleCarBeginsChargingEvent(currEvent, currState):
    currCar = currEvent.data
    currCar.timeStartCharging = currEvent.time

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    currParkingPlace.startCharging()

    # Calculate how much time to finish charging without interruption
    return [event.Event(time=currEvent.time + currCar.chargingVolume / (6 / 3600), eventType="carStopsCharging", data=currCar)]


def handleCarStopsChargingEvent(currEvent, currState):
    currCar = currEvent.data

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    currParkingPlace.stopCharging()

    # Calculate how much was charged
    currCar.amountCharged = (
        6/3600) * (currEvent.time - currCar.timeStartCharging)
    return []


def handleCarArrivalEvent(currEvent, currState):
    currCar = currEvent.data
    currCar.carParksVisited.append(currCar.parkingPlaceID)

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    if currParkingPlace.isFull():
        return handleCarPlaceFull(currEvent, currState)

    currParkingPlace.arriveAtCharger()
    # Use the carBeginsChargingEvent for later addition of the not base cases. Also schedule the planned leave
    return [event.Event(time=currEvent.time, eventType="carBeginsCharging", data=currCar),
            event.Event(time=currEvent.time + currCar.connectionTime, eventType="carPlannedLeave", data=currCar)]


# NOT AN EVENT, but an helper function for clarity
def handleCarPlaceFull(currEvent, currState):
    currCar = currEvent.data

    # As specified in assignment, stop visiting
    if len(currCar.carParksVisited) == 3:
        logger.logMessage("Too many Car Places (3) full in a row")
        currState["carsUnableCharged"] += 1
        return []

    # TODO normal distributed travel time to other parkingPlace
    timeToTravel = 10 * 60

    # Get new parking place, and schedule a new event after certain amount of time
    currCar.parkingPlaceID = generator.generateParkingPlace(
        currCar.carParksVisited)

    logger.logMessage("Car Place full, moving to another")
    currState["carsAtFullParking"] += 1
    return [event.Event(time=currEvent.time + timeToTravel, eventType="carArrives", data=currCar)]


# Occurs when the car has finished charging
def handleCarLeavesEvent(currEvent, currState):
    currCar = currEvent.data

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    currParkingPlace.leaveCharger()
    currState["carsCharged"] += 1

    return []

# TODO


def handleSolarUpdateEvent(currEvent, currState):
    return []
