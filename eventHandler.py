def eventHandler(eventQueue):
    next_item = eventQueue.get()

    currEvent = next_item[1]
    if currEvent == Events.ArriveCar:
        eventQueue.put((next_item[0] + 5, "LeaveCar"))
    elif currEvent == Events.CarLeave:
        print("Leaving")
