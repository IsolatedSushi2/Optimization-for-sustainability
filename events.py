class Events(Enum):
    CarArrives = 0 
    CarPlannedLeave = 1
    CarCharge = 2
    CarLeave = 3
    SolarPowerUpdate = 4



def eventHandler(eventQueue):
    next_item = eventQueue.get()

    currEvent = next_item[1]
    if currEvent == Events.ArriveCar:
        eventQueue.put((next_item[0] + 5, "LeaveCar"))
    elif currEvent == Events.CarLeave:
        print("Leaving")
