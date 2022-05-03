import numpy as np
from events import Events

def generateCarArrivalTimes(arrival_data, carAmount):
    # weights = arrival_data[:,1] * carAmount
    # samples = np.random.poisson(weights)

    randomArrivals = np.random.uniform(0, 24 * 3600, carAmount)
    return randomArrivals

def generateParkingLocations(parking_distribution, carAmount):

    randomPlaces = np.random.randint(1, 8, carAmount)
    return randomPlaces

def generateRandomCharges(charging_distribution, carAmount):

    randomCharges = np.random.randint(0, 102, carAmount)
    return randomCharges

def generateRandomConnectionTimes(connection_distribution, carAmount):

    randomConnectionTimes = np.random.randint(0, 71, carAmount)
    return randomConnectionTimes


def generateCarArrivalEvents(arrival_data, parking_distribution, charging_distribution, connection_distribution, carAmount):
    randomTimes = generateCarArrivalTimes(arrival_data, carAmount)
    randomLocations = generateParkingLocations(parking_distribution, carAmount)
    randomCharges = generateRandomCharges(charging_distribution, carAmount)
    randomConnectionTimes = generateRandomConnectionTimes(connection_distribution, carAmount)

    eventData = zip(randomLocations, randomCharges, randomConnectionTimes)
    eventIDS = [Events.CarArrives] * carAmount
    
    arrivalEvents = zip(eventIDS, eventData)
    return zip(randomTimes, arrivalEvents)



