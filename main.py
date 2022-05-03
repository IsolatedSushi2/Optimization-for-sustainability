from dataReader import readCSVs
import generator
import dataReader as dr
import simulator
import logger
import time
def main():
    logger.clearLog()

    startTime = time.time()
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventQueue = generator.generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions, timeLength=24)
    simulator.startSimulation(eventQueue)
    print("Simulation took", time.time() - startTime, "seconds")

if __name__ == "__main__":
    main()
