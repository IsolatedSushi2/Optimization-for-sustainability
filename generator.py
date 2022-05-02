import numpy as np
import dataReader as dr
from queue import PriorityQueue

def generateCar():
    pass

def generateSolarValue(timeOfDay, solar_availability_distributions, season='summer'):
    # returns a randomly generated value for available power from a solar panel array at the specified time of day in the specified season (summer/winter)
    timeOfDay = timeOfDay%24
    if season=='summer':
        solar_power = solar_availability_distributions[timeOfDay,2] * 200
    else:
        solar_power = solar_availability_distributions[timeOfDay,1] * 200
    return np.random.normal(solar_power, 0.15*solar_power)

def generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions, average_daily_cars, timeLength = 24, season='summer'):
    # N.B. timeLength input is in HOURS not in seconds

    generatedEvents = PriorityQueue()

    # Generate car arrivals
    for t in range(timeLength):
        allMoments = np.random.poisson(average_daily_cars*arrival_fractions[t,1], size=3600)
        newCarsIndices = np.where(allMoments>0)[0] #use this to find the indices in the array where the value is nonzero (i.e. one or more cars arrive)
        for time in newCarsIndices:
            for newCar in range(allMoments[time]):
                # Loop is needed in case two cars arrive the very same second.
                generatedEvents.put((t*3600+time, ("carArrives", (generateCar()) ) ))

    # Generate solar events
    for t in range(timeLength):
        generatedEvents.put((t*3600, ("solarUpdate", (generateSolarValue(t, solar_availability_distributions, season)) ) ))

    return generatedEvents

