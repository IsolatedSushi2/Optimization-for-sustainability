
from ast import Assert
from distutils.filelist import findall
from math import sqrt
import numpy as np
import performanceMeasures

def writeTable(data, file, header = "Data Table: \\\\ \hline \n"):
    with open(f'./tables/{file}', 'a') as myfile:
        myfile.write(header)
        for line in data:
            newline = ""
            for element in line:
                newline += f" & {element}"
            newline += " \\\\ \n"
            myfile.write(newline[3:])
        myfile.write("\n ---- \n")

def emptyList(h,w):
    lst = []
    for i in range(h):
        lst.append([None]*w)
    return lst

def findAllPairedConfidenceIntervals(cases, file = 'tables.txt', params = ["maxDelay", "avgDelay", "percentDelayed", "maxLoad0", "overload0", "blackout0", "maxLoad1", "overload1", "blackout1", "percentNonServiced", "avgDailyNonServiced"]):
    resultsDict = {}
    for case in cases:
        print(f'finding {case} measures')
        if case not in resultsDict:
            resultsDict[case] = {}

        resultsDict[case]["maxDelay"], resultsDict[case]["avgDelay"], resultsDict[case]["percentDelayed"] = findDelays(case)
        cable0, cable1, cable2, cable3, cable4, cable5, cable6, cable7, cable8 = findCableLoads(case)
        resultsDict[case]['maxLoad0'], resultsDict[case]['overload0'], resultsDict[case]['blackout0'] = cable0
        resultsDict[case]["maxLoad1"], resultsDict[case]["overload1"], resultsDict[case]["blackout1"] = cable1
        resultsDict[case]["maxLoad2"], resultsDict[case]["overload2"], resultsDict[case]['blackout2'] = cable2
        resultsDict[case]['maxLoad3'], resultsDict[case]['overload3'], resultsDict[case]['blackout3'] = cable3
        resultsDict[case]['maxLoad4'], resultsDict[case]['overload4'], resultsDict[case]['blackout4'] = cable4
        resultsDict[case]['maxLoad5'], resultsDict[case]['overload5'], resultsDict[case]['blackout5'] = cable5
        resultsDict[case]['maxLoad6'], resultsDict[case]['overload6'], resultsDict[case]['blackout6'] = cable6
        resultsDict[case]['maxLoad7'], resultsDict[case]['overload7'], resultsDict[case]['blackout7'] = cable7
        resultsDict[case]['maxLoad8'], resultsDict[case]['overload8'], resultsDict[case]['blackout8'] = cable8
        resultsDict[case]['percentNonServiced'], resultsDict[case]['avgDailyNonServiced'] =  findNonServiced(case)

    amountCases = len(cases)
    for param in params:
        print(f'creating {param} table')
        allConfidenceIntervals = emptyList(amountCases+1, amountCases+1)
        allConfidenceIntervals[0][0] = ' '
        for i in range(amountCases):
            #write column/row headers
            allConfidenceIntervals[i+1][0] = cases[i]
            allConfidenceIntervals[0][i+1] = cases[i]
            for j in range(amountCases):
                case1 = cases[i]
                case2 = cases[j]
                allConfidenceIntervals[i+1][j+1] = get_paired_confidence_interval(resultsDict[case1][param], resultsDict[case2][param])
        writeTable(allConfidenceIntervals, file=file, header=f"Paired Confidence Intervals of {param} \n")

def s2(xs):
    average = sum(xs)/len(xs)
    diffs2 = sum([(x-average)**2 for x in xs])
    return diffs2 / (len(xs) - 1)

def get_paired_confidence_interval(xs1, xs2):
    assert len(xs1) == len(xs2) 
    n = len(xs1)
    z = [xs2[i] - xs1[i] for i in range(n)]
    z_bar = sum(z) / n
    s_z2 = sum([(z_j - z_bar)**2 for z_j in z]) / (n - 1)
    t = 2.262 # for n=10, alpha = 0.05 
    plusminus = t * sqrt(s_z2/n)
    return (z_bar - plusminus, z_bar + plusminus)


def readFile(path):

    returnTimestamps = []
    returnDataPoints = []    

    timestamps = []
    dataPoints = []
    with open(path, "r") as file:
        lines = file.readlines()

        for line in lines[1:]:
            if(line[0] == '-'):
                # print("Results of new simulation")
                returnTimestamps.append(timestamps)
                returnDataPoints.append(dataPoints)

                timestamps = []
                dataPoints = []
            else:
                tokens = line.split(',')
                tokens = [float(curr) for curr in tokens]
                timestamps.append(tokens[0])
                dataPoints.append(tokens[1:])

    return returnTimestamps, returnDataPoints


def findDelays(root):
    with open(f"./{root}/delays.txt", "r") as file:
        lines = file.readlines()


    allData = []
    currSimulationData = []
    for line in lines[1:]:
        if line[0] == '-':
            allData.append(currSimulationData)
            currSimulationData = []
        else:
            currSimulationData.append(float(line.split(',')[1].strip()))
    # Max delay, Average delay, percentage with delay
    results = ([],[],[])
    for parsed in allData:
        parsed = np.array(parsed)
        results[0].append(np.max(parsed)) # max delay
        results[1].append(np.mean(parsed)) # average delay
        results[2].append(100 * parsed[parsed!=0.0].shape[0] / parsed.shape[0]) # percentage delayed
        # print(parsed)
        # print("Minimum delay:", np.min(parsed))
        # print("Maximum delay:", np.max(parsed))
        # print("Average delay:", np.mean(parsed))
        # print("Percentage with delay:", 100 * parsed[parsed!=0.0].shape[0] / parsed.shape[0])
        # print("Percentage without delay:", 100 * parsed[parsed==0.0].shape[0] / parsed.shape[0])
    return results 

def findCableLoads(root):
    allTimestamps, allCablePower = readFile(f'./{root}/powerDensity.txt')
    
    #[max, % overload, % blackout] for each cable
    results = (([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]), ([],[],[]))
    for simulationIndex in range(len(allTimestamps)):
        timesteps = allTimestamps[simulationIndex]
        cablePower = allCablePower[simulationIndex]
        cablePower = np.array(cablePower).T

        finalTimestep = timesteps[-1]
        firstTimeStep = timesteps[0]
        for i in range(9):
            maxValue = max(cablePower[i])
    
            atLeast10 = 0
            max10 = 0
            noOverload = 0

            # Calculate how long the overloads last
            for j in range(len(timesteps) - 1):
                if cablePower[i][j] >= 1.1 * 200:
                    atLeast10 += timesteps[j+1] - timesteps[j]
                elif cablePower[i][j] >= 1 * 200: 
                    max10 += timesteps[j+1] - timesteps[j]
                else:
                    noOverload += timesteps[j+1] - timesteps[j]


            #Divide to get the fraction
            atLeast10 /= (finalTimestep - firstTimeStep)
            max10 /= (finalTimestep - firstTimeStep)
            noOverload /= (finalTimestep - firstTimeStep)

            assert abs(atLeast10 + max10 + noOverload - 1.0) < 0.01

            results[i][0].append(maxValue)
            results[i][1].append(max10)
            results[i][2].append(atLeast10)
    return results 

def findNonServiced(root, simLength=10*86400, cutStart = 2*86400, cutEnd = 1*86400):
    with open(f"./{root}/serviced.txt", "r") as file:
        lines = file.readlines()
    # % non serviced, average daily non serviced
    results = ([],[])

    totalServed = 0
    totalNonServed = 0
    for line in lines:
        if (line[0] == "-") and (totalServed + totalNonServed > 0):
            results[0].append(100*totalNonServed/(totalNonServed + totalServed))
            results[1].append(86400*totalNonServed/(simLength-cutStart - cutEnd))
            totalNonServed = 0
            totalServed = 0
        elif line[0].isdigit():
            timeStamp, isServed = line.split(',')
            timeStamp = int(timeStamp)
            isServed = isServed.strip()
            if cutStart < timeStamp < simLength - cutEnd:
                if isServed.lower() == "served":
                    totalServed += 1
                elif isServed.lower() == "notserved":
                    totalNonServed += 1
                else:
                    raise AssertionError
        

    return results 

findAllPairedConfidenceIntervals(cases = ['base','base-summer-1-2-6-7', 'base-summer-6-7','base-winter-1-2-6-7','base-winter-6-7'], file='base-different-solars.txt')
findAllPairedConfidenceIntervals(cases = ['ELFS','ELFS-summer-1-2-6-7','ELFS-summer-6-7','ELFS-winter-1-2-6-7','ELFS-winter-6-7'], file='ELFS-different-solars.txt')
findAllPairedConfidenceIntervals(cases = ['FCFS','FCFS-summer-1-2-6-7','FCFS-summer-6-7','FCFS-winter-1-2-6-7','FCFS-winter-6-7'], file='FCFS-different-solars.txt')
findAllPairedConfidenceIntervals(cases = ['base', 'ELFS','FCFS'], file = 'different-no-solar.txt')
findAllPairedConfidenceIntervals(cases = ['base-summer-1-2-6-7','ELFS-summer-1-2-6-7', 'FCFS-summer-1-2-6-7'], file = 'different-summer-1-2-6-7.txt')
findAllPairedConfidenceIntervals(cases = ['base-summer-6-7','FCFS-summer-6-7','ELFS-summer-6-7'], file = 'different-summer-6-7.txt')
findAllPairedConfidenceIntervals(cases = ['base-winter-1-2-6-7','ELFS-winter-1-2-6-7', 'FCFS-winter-1-2-6-7'], file = 'different-winter-1-2-6-7.txt')
findAllPairedConfidenceIntervals(cases = ['base-winter-6-7','FCFS-winter-6-7','ELFS-winter-6-7'], file = 'different-winter-6-7.txt')