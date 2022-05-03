from dataReader import readCSVs
import generator
import dataReader as dr
import simulator
import logger
def main():
    logger.clearLog()
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventQueue = generator.generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions)

    simulator.startSimulation(eventQueue)


if __name__ == "__main__":
    main()
