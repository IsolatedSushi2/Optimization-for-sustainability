class ParkingPlace():
    maxNumberCharginStations: int
    amountCurrentlyParked: int

    def __init__(self, maxNumberCharginStations):
        self.maxNumberCharginStations = maxNumberCharginStations
        self.amountCurrentlyParked = 0
        self.amountCurrentlyCharging = 0

    def startCharging(self):
        assert self.amountCurrentlyCharging + 1 <= self.amountCurrentlyParked
        self.amountCurrentlyCharging += 1

    def stopCharging(self):
        assert self.amountCurrentlyCharging > 0
        self.amountCurrentlyCharging -= 1

    def arriveAtCharger(self):
        assert self.amountCurrentlyParked <= self.maxNumberCharginStations
        self.amountCurrentlyParked += 1

    def leaveCharger(self):
        assert self.amountCurrentlyParked > 0
        self.amountCurrentlyParked -= 1

    def isFull(self):
        return self.maxNumberCharginStations == self.amountCurrentlyParked

#Creates the parking places, using strings for the IDS
def createParkingPlaces():
    chargingStationAmounts = [60, 80, 60, 70, 60, 60, 50]
    parkingPlaces = {}
    for index in range(7):
        parkingPlaceIndex = str(index+1)
        parkingPlaces[parkingPlaceIndex] = ParkingPlace(maxNumberCharginStations=chargingStationAmounts[index])
    return parkingPlaces
