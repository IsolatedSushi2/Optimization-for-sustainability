def printMaximumCableLoad(currState):
    powerPerTimestep = currState["powerDrawnPerTimeStep"]

    powerPerCablePerStep = [calculateChargePerCable(curr[1]) for curr in powerPerTimestep]
    
    cablePowerDict = chargeDictToLists(powerPerCablePerStep)

    for i in range(9):
        cableName = "cable" + str(i)
        print("Max value for", cableName, "is: ", max(cablePowerDict[cableName]))


def print10OverloadPercentage(currState):
    powerPerTimestep = currState["powerDrawnPerTimeStep"]

    powerPerCablePerStep = [calculateChargePerCable(curr[1]) for curr in powerPerTimestep]
    cablePowerDict = chargeDictToLists(powerPerCablePerStep)

    timesteps = [curr[0] for curr in powerPerTimestep]

    finalTimestep = timesteps[-1]

   
    for i in range(9):
        atLeast10 = 0
        max10 = 0
        noOverload = 0

        cableName = "cable" + str(i)
        for j in range(len(timesteps) - 1):
            if cablePowerDict[cableName][j] >= 1.1 * 200:
                atLeast10 += timesteps[j+1] - timesteps[j]
            elif cablePowerDict[cableName][j] >= 1 * 200: 
                max10 += timesteps[j+1] - timesteps[j]
            else:
                noOverload += timesteps[j+1] - timesteps[j]

        atLeast10 /= finalTimestep
        max10 /= finalTimestep
        noOverload /= finalTimestep
        
        print("For cable", cableName, "at least 10% overload:", atLeast10, ", at most 10% overload", max10, "and no overload", noOverload)
        print("check summation==1:", atLeast10 + max10 + noOverload)

            


def chargeDictToLists(powerPerCablePerStep):
    
    returnDict = {}
    for i in range(9):
        returnDict["cable" + str(i)] = []

    for currPowerCharge in powerPerCablePerStep:
        for cable, powerDrawn in currPowerCharge.items():
            returnDict[cable].append(powerDrawn)

    return returnDict




def calculateChargePerCable(chargePerTimestep):
    cables = {}
    cables["cable1"] = chargePerTimestep[0]
    cables["cable2"] = chargePerTimestep[1]
    cables["cable3"] = chargePerTimestep[2]
    cables["cable5"] = chargePerTimestep[6]
    cables["cable7"] = chargePerTimestep[4]
    cables["cable8"] = chargePerTimestep[5]
    
    # Compound cables
    cables["cable6"] = cables["cable7"] + cables["cable8"]
    cables["cable4"] = cables["cable6"] + cables["cable5"] + chargePerTimestep[3]
    cables["cable0"] = cables["cable1"] + cables["cable2"] + cables["cable3"]
    

    return cables