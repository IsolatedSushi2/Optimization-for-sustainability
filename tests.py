from generator import generateAllEvents
import dataReader as dr
import event
import matplotlib.pyplot as plt
import numpy  as np

def testCarArrivals():
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventsQueue = generateAllEvents(arrival_fractions, charging_volume_distributions,
                                    connection_time_distributions, solar_availability_distributions)

    carArrivalTimes = []

    while (not eventsQueue.empty()):
        a = eventsQueue.get()  # throw away one event
        if a.eventType == "carArrives":
            carArrivalTimes.append(a.time)


    plt.hist(np.array(carArrivalTimes) / 3600, density=True, bins=24)
    plt.show()

def testCarConnectionTimes():
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventsQueue = generateAllEvents(arrival_fractions, charging_volume_distributions,
                                    connection_time_distributions, solar_availability_distributions)

    carConnectionTimes = []

    while (not eventsQueue.empty()):
        a = eventsQueue.get()  # throw away one event
        if a.eventType == "carArrives":
            carConnectionTimes.append(a.data.connectionTime)
    carConnectionTimes = np.array(carConnectionTimes)
    print(np.mean(carConnectionTimes))

def main():
    testCarConnectionTimes()


if __name__ == "__main__":
    main()
