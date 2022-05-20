from dataReader import readCSVs
import generator
import dataReader as dr
import simulator
import logger
import state
import showPlots

def main():
    # Clear the files for a new run
    logger.clearLog()
    state.clearPerformanceFiles()

    #Generate the distributions, events and start the simulation
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventQueue = generator.generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions, timeLength=24 * 1)
    currState = simulator.startSimulation(eventQueue, "FCFS")

    #Show the results
    state.printResults(currState)
    showPlots.showPlots(currState)

if __name__ == "__main__":
    main()
