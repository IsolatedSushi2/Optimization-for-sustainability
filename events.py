from enum import Enum


class Events(Enum):
    CarArrives = 0 
    CarPlannedLeave = 1
    CarCharge = 2
    CarLeave = 3
    SolarPowerUpdate = 4   


# Event of the form: (EventID, (EventData))
def eventHandler(eventQueue):
    next_item = eventQueue.get()

    currEvent = next_item[1]
    if currEvent == Events.ArriveCar:
        eventQueue.put((next_item[0] + 5, "LeaveCar"))
    elif currEvent == Events.CarLeave:
        print("Leaving")
