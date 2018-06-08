import math

def haversine(pointA,pointB):
    radius = 6371
    thetaA = math.radians(pointA[0])
    thetaB = math.radians(pointB[0])
    deltaLat = math.radians(pointB[0]-pointA[0])
    deltaLon = math.radians(pointB[1] - pointA[1])

    a = (math.sin(deltaLat/2))**2 + \
        math.cos(thetaA)* math.cos(thetaB) * \
        (math.sin(deltaLon/2))**2
    b = 2 * math.asin(math.sqrt(a))
    c = radius * b
    return c



def get_distanceList(pointList, pointA):
    distanceDict= {}
    for pointB in pointList:
        distance = haversine(pointA,pointB[1])
        pointB[1].append(distance)
        distanceDict[pointB[0]] = pointB[1]
    return distanceDict


