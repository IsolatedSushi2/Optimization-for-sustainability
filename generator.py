import numpy as np

def generateCarArrivals(arrival_data, carAmount):
    weights = arrival_data[:,1] * carAmount
    print(weights)
    samples = np.random.poisson(weights)
    print(samples)


    print(np.sum(samples))

