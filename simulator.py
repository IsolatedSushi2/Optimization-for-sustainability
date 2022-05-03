def startSimulation(eventQueue):

    while not eventQueue.empty():
        next_item = eventQueue.get()

        print(next_item.data[0])
