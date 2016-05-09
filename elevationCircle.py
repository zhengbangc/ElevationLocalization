# Copyright Google Inc. 2010 All Rights Reserved
import simplejson
import urllib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

ELEVATION_BASE_URL = 'http://maps.google.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.googleapis.com/chart'

def getElevation(pointsStr,coordX, coordY, ax, lowest_elevation, samples="100",sensor="false", **elvtn_args):
    elvtn_args.update({
        'locations': pointsStr,
        # 'samples': samples,
        'sensor': sensor
    })

    url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args)
    # print url
    response = simplejson.load(urllib.urlopen(url))


    # Create a dictionary for each results[] object
    elevationArray = []
    for resultset in response['results']:
      elevationArray.append(resultset['elevation'])

        
    X = coordX
    Y = coordY
    Z = elevationArray
    i = 0;
    while i < len(X):
        if Z[i] < lowest_elevation:
            lowest_elevation = Z[i]
        ax.scatter(X[i], Y[i], Z[i], c='b', marker='o')
        i = i+1
    return lowest_elevation


# Helper function for getPointsEvenly()
def rtpairs(r, n):
    for i in range(len(r)):
       for j in range(n[i]):    
        yield r[i], j*(2 * np.pi / n[i])

#this function takes in a coordinate's latitude, longitude, and an array to contain all the points generated
#T specified the number of points at a certain radius and R is an arry of possible radius
#Might need to change the numbers because 1) 512 points per request limit 2)the error range of GSM tower might be different
def getPointsEvenly(latitude, longitude, pointsStr, coordX, coordY):
    T = [1, 5,10,15, 20,25, 30,35, 40,45, 50,55, 60] #sum should < 512
    R = [0.0,5, 10,15, 20,25,30,35,40,45, 50,55, 60]
    count = 0
    lowest_elevation = 1000
    zscale = 5
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for r, t in rtpairs(R, T):
        cur_latitude = latitude + (r*np.cos(t))/6378000*(180/np.pi)
        cur_longitude = longitude + (r*np.sin(t))/6378000*(180/np.pi)/np.cos(latitude*np.pi/180)
        coordX.append(cur_latitude)
        coordY.append(cur_longitude)
        pointsStr += str(cur_latitude)+","+ str(cur_longitude) + "|"
        count = count + 1
        if(count % 50 == 0):
            pointsStr = pointsStr[:-1]
            lowest_elevation = getElevation(pointsStr, coordX, coordY, ax, lowest_elevation)
            coordX = []
            coordY = []
            pointsStr = ""
    pointsStr = pointsStr[:-1]
    lowest_elevation = getElevation(pointsStr, coordX, coordY, ax, lowest_elevation)
    coordX = []
    coordY = []
    pointsStr = ""

    ax.set_xlabel("latitude")
    ax.set_ylabel("longitude")
    ax.set_zlabel("elevation")
    ax.set_zlim3d(lowest_elevation, lowest_elevation+zscale)
    # ax.set_autoscale_on(False)

    plt.show()
    return pointsStr


if __name__ == '__main__':

    # Collect the Latitude/Longitude input string
    # from the user
    latitude = raw_input('Enter the latitude of your current location:   ')
    if not latitude:
      latitude = 40.089513

    longitude = raw_input('Enter the longitude of your current location:    ')
    if not longitude:
      longitude = -88.239050

    coordX = []
    coordY = []
    pointsStr = ""
    pointsStr = str(getPointsEvenly(float(latitude), float(longitude), pointsStr, coordX, coordY))
    # getElevation(pointsStr, coordX, coordY)
