path = "./logs/log.txt"

def clearLog():
    file = open(path,"w")
    file.close()

def logEvent(currEvent):
    logging = "Event: {eventType} at time {eventTime}"
    message = logging.format(eventType=currEvent.eventType, eventTime=currEvent.time)
    logMessage(message)
    
def logMessage(message):
    with open(path, "a") as myfile:     
        myfile.write(message + "\n")
