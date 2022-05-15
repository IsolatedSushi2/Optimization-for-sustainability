from distutils.log import error
import event
import state
import generator
import logger
import showPlots
import performanceMeasures
import time

# Start the simulation
def startSimulation(eventQueue):

    # The eventhandlers allow the events to be mapped to their handlers
    eventHandlers = {"carArrives": handleCarArrivalEvent,
                     "carExpectedStopCharging": handleCarExpectedStopChargingEvent,
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

        # End the simulation when we encounter the endSimulation event
        # if currEventType == "endSimulation":
        #     break 

        assert currEventType in eventHandlers

        # Some events may schedule new events, schedule those here
        returnEvents = eventHandlers[currEventType](currEvent, currState)
        for returnEvent in returnEvents:
            eventQueue.put(returnEvent)

        # Log every event for debugging
        state.storeDataPerTimestep(currEvent.time, currState)
        logger.logEvent(currEvent)

    print("Simulation took", time.time() - startTime, "seconds")
    
    return currState

def handleCarPlannedLeaves(currEvent, currState): 
    currCar = currEvent.data

    chargedSinceLastStart = 0
    if currCar.timeStartCharging:
        chargedSinceLastStart = (6/3600) * (currEvent.time - currCar.timeStartCharging)

    totalCharge = currCar.amountCharged + chargedSinceLastStart
    
    # Is finished charging
    if totalCharge >= currCar.chargingVolume:
        logger.logMessage(f'Car {currCar.carID}, succesfully charged')
        return [event.Event(time=currEvent.time, eventType="carLeaves", data=currCar)]
    # Hasn't finished charging, but is busy charging
    else:
        logger.logMessage(
            f'Car {currCar.carID}, not succesfully charged. ERROR in basecase')
        return [event.Event(time=currEvent.time + (currCar.chargingVolume - totalCharge) / (6/3600), eventType="carPlannedLeave", data=currCar)]


def handleCarBeginsChargingEvent(currEvent, currState):
    currCar = currEvent.data
    currCar.timeStartCharging = currEvent.time

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    # TODO: update the line below when parking places keep track of all cars parked/charging there
    currParkingPlace.startCharging()

    # Calculate how much time to finish charging without interruption
    return [event.Event(time=currEvent.time + (currCar.chargingVolume - currCar.amountCharged) / (6 / 3600), eventType="carExpectedStopCharging", data=currCar)]


def handleCarStopsChargingEvent(currEvent, currState):
    currCar = currEvent.data

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    # TODO: update the line below when parking places keep track of all cars parked/charging there
    currParkingPlace.stopCharging()

    # Calculate how much was charged
    currCar.amountCharged += (6/3600) * (currEvent.time - currCar.timeStartCharging)
    currCar.timeStartCharging = None

    if currState['chargingStrategy'] == ('base' or 'price-driven'):
        return []
    elif currState['chargingStrategy'] == 'FCFS':
        pass # TODO: implement scheduling of another car's charging when current car stops charging
    elif currState['chargingStrategy'] == 'ELFS': 
        pass # TODO: implement scheduling of another car's charging when current car stops charging

def handleCarArrivalEvent(currEvent, currState):
    currCar = currEvent.data
    currCar.carParksVisited.append(currCar.parkingPlaceID)

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    if currParkingPlace.isFull():
        return handleCarPlaceFull(currEvent, currState)

    # TODO: update the line below when parking places keep track of all cars parked/charging there
    currParkingPlace.arriveAtCharger()
    # Use the carBeginsChargingEvent for later addition of the not base cases. Also schedule the planned leave
    assert currState['chargingStrategy'] in {'base', 'price-driven', 'FCFS', 'ELFS'}
    if currState['chargingStrategy'] == 'base':
        return [event.Event(time=currEvent.time, eventType="carBeginsCharging", data=currCar),
            event.Event(time=currEvent.time + currCar.connectionTime, eventType="carPlannedLeave", data=currCar)]
    elif currState['chargingStrategy'] == 'price-driven':
        return [event.Event(time=findCheapestTime(currEvent, currState), eventType="carBeginsCharging", data=currCar),
            event.Event(time=currEvent.time + currCar.connectionTime, eventType="carPlannedLeave", data=currCar)]
    elif currState['chargingStrategy'] == 'FCFS':
        pass # TODO: implement charging planning with FCFS strategy
    elif currState['chargingStrategy'] == 'ELFS':
        pass # TODO: implement charging planning with ELFS strategy

# NOT AN EVENT, but a helper function for clarity
def findCheapestTime(currEvent, currState):
    def findCost(startTime, duration):
        endTime = startTime + duration 

        cost = 0
        for t in range(startTime, endTime): # Good grief, this is ugly but it's hot and I'm tired. Let's improve this another day
            t = t  % (24*3600)
            if 0 <= t < 8*3600:
                cost += 16 / (3600/6)
            elif 8*3600 <= t < 16*3600:
                cost += 18 / (3600/6)
            elif 16*3600 <= t < 20*3600:
                cost += 22 / (3600/6)
            elif 20*3600 <= t < 24*3600:
                cost += 20 / (3600/6)
        return cost 

    currCar = currEvent.data
    chargingTime = currCar.chargingVolume /(6/3600)
    firstTime = currEvent.time
    lastTime = firstTime + currCar.connectionTime - chargingTime
    
    timesToCheck = [firstTime, lastTime] 
    generateMoreTimes = True 
    days = firstTime // (24*3600)
    while generateMoreTimes:
        times = [days, days + 8*3600, days+16*3600, days+20*3600]
        for time in times:
            if firstTime < time < lastTime:
                timesToCheck.append(time)
        if days + 20*3600 > lastTime:
            generateMoreTimes = False 
        days += 1

    lowestCost = currCar.chargingVolume * 22 + 1 #Higher than the highest possible cost
    cheapestStartTime = None

    for time in timesToCheck:
        cost = findCost(time,chargingTime)
        if cost < lowestCost:
            lowestCost = cost
            cheapestStartTime = time

    return cheapestStartTime

# NOT AN EVENT, but an helper function for clarity
def handleCarPlaceFull(currEvent, currState):
    currCar = currEvent.data

    # As specified in assignment, stop visiting
    if len(currCar.carParksVisited) == 3:
        logger.logMessage("Too many Car Places (3) full in a row")
        currState["carsUnableCharged"] += 1
        return []


    # Get new parking place, and schedule a new event after certain amount of time
    currCar.parkingPlaceID = generator.generateParkingPlace(
        currCar.carParksVisited)

    logger.logMessage("Car Place full, moving to another")
    currState["carsAtFullParking"] += 1
    return [event.Event(time=currEvent.time, eventType="carArrives", data=currCar)]


# Occurs when the car has finished charging
def handleCarLeavesEvent(currEvent, currState):
    currCar = currEvent.data

    currParkingPlace = currState["parkingPlaces"][currCar.parkingPlaceID]
    # TODO: update the line below when parking places keep track of all cars parked/charging there
    currParkingPlace.leaveCharger()
    currState["carsCharged"] += 1

    return []


# TODO
def handleSolarUpdateEvent(currEvent, currState):
    for currParkingPlace in currState["parkingPlaces"].values():
        currParkingPlace.setSolarPower(currEvent.data)
    if currState['chargingStrategy'] == ('base' or 'price-driven'):
        return []
    elif currState['chargingStrategy'] == 'FCFS':
        pass # TODO: implement scheduling more/less car charging after solar update
    elif currState['chargingStrategy'] == 'ELFS': 
        pass # TODO: implement scheduling more/less car charging after solar update

def handleCarExpectedStopChargingEvent(currEvent, currState):
    currCar = currEvent.data 
    if currCar.timeStartCharging:
        chargedSinceLastStart = (currEvent.time - currCar.timeStartCharging) * (6/3600)
        if currCar.amountCharged + chargedSinceLastStart >= currCar.chargingVolume:
            return []
        else:
            return [event.Event(time=currEvent.time + (currCar.chargingVolume - currCar.amountCharged - chargedSinceLastStart) / (6 / 3600), eventType="carExpectedStopCharging", data=currCar)]
    return []
