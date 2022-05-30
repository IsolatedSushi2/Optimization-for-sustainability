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

    simulationAmount = 2
    for index in range(simulationAmount):
        currState = runSimulation(index)

    state.storeSimulationHeader("END")
    state.printResults(currState)
    showPlots.showPlots(currState)
    showPlots.printDelays()


def runSimulation(index):
    print("Running Simulation", index)
    state.storeSimulationHeader(index)
    #Generate the distributions, events and start the simulation
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventQueue = generator.generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions, timeLength=24 * 3)
    currState = simulator.startSimulation(eventQueue, "base")#, ["6", "7"] )

    #Show the results
    

    return currState



if __name__ == "__main__":
    main()
