from dataReader import readCSVs
import generator
import dataReader as dr
import simulator
import logger
import state
import showPlots
import os

def main(strategy = 'base', solarPanels = [], season = 'summer'):


    path_root = os.getcwd()
    target_dir = f'{strategy}'
    if solarPanels != []:
        target_dir = f'{strategy}-{season}'
        for panel in solarPanels:
            target_dir += f'-{panel}'
    combined_dir = os.path.join(path_root, target_dir)
    if not os.path.isdir(combined_dir):
        # Clear the files for a new run
        logger.clearLog()
        state.clearPerformanceFiles()
        simulationAmount = 10
        for index in range(simulationAmount):
            currState = runSimulation(index, strategy = strategy, solarPanels = solarPanels, season = season)

        state.storeSimulationHeader("END")

        
        os.mkdir(combined_dir)
        state.movePerformanceFiles(combined_dir)
    else:
        print(f'folder already exists: {combined_dir}')
    #state.printResults(currState)
    #showPlots.showPlots(currState)
    #showPlots.printDelays()


def runSimulation(index, strategy = 'base', solarPanels = [], season = 'summer'):
    print("Running Simulation", index)
    state.storeSimulationHeader(index)
    #Generate the distributions, events and start the simulation
    arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions = dr.readCSVs()
    eventQueue = generator.generateAllEvents(arrival_fractions, charging_volume_distributions, connection_time_distributions, solar_availability_distributions, timeLength=24 * 10, season=season)
    currState = simulator.startSimulation(eventQueue, strategy, parkingPlacesWithPanelsID=solarPanels)

    #Show the results
    

    return currState



if __name__ == "__main__":
    # curr = state.createInitialState()
    # showPlots.showChargeDensity(curr)
    for strategy in ['base', 'FCFS', 'ELFS']:
        for solarPanels in [[],['6','7'],['1','2','6','7']]:
            for season in ['summer','winter']:
                if not (solarPanels == [] and season == 'winter'): #prevent running duplicate simulation for different seasons when there's no solar panels anyway
                    main(strategy=strategy, solarPanels=solarPanels,season=season)

    # main()
