# Copyright Google Inc. 2010 All Rights Reserved
import simplejson
import urllib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import csv
import operator
import time

ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.googleapis.com/chart'

# Obtain data from csv file
Path_CSV = open("paths/07-35-16_12:35:51_MSFINAL.csv")
CSV_Reader = csv.reader(Path_CSV)
Path_List = list(CSV_Reader) #the third column are elevations
print len(Path_List)



def getElevation(pointsStr,coordX, coordY, ax, lowest_elevation, points_z, samples="100",sensor="false", **elvtn_args):
    elvtn_args.update({
        'locations': pointsStr,
        # 'samples': samples,
        'sensor': sensor
    })

    url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args) + '&key=AIzaSyBgiEsyAW3QsOIINxTCEv8o4ZQmog6F14Q'
    # url = "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=AIzaSyDxBVLVXChcMc0DvFZTtaMTS3J7UV5CCJE"
    response = simplejson.load(urllib.urlopen(url))
    # Create a dictionary for each results[] object
    elevationArray = []
    for resultset in response['results']:
      elevationArray.append(resultset['elevation'])
      points_z.append(resultset['elevation'])

        
    X = coordX
    Y = coordY
    Z = elevationArray

    i = 0;
    while i < len(X):
        if Z[i] < lowest_elevation:
            lowest_elevation = Z[i]
        #add points to the graph
        # ax.scatter(X[i], Y[i], Z[i], c='b', marker='o')
        i = i+1
    return lowest_elevation

# Helper function for getPointsEvenly()
def rtpairs(r, n):
    for i in range(len(r)):
       for j in range(n[i]):    
        yield r[i], j*(2 * np.pi / n[i])

#this function takes in a coordinate's latitude, longitude, and an array to contain all the points generated
#T specified the number of points at a certain radius and R is an arry of possible radius
def getPointsEvenly(latitude, longitude, pointsStr, points_x, points_y, points_z, lowest_elevation):
    T = [1, 5,10,15, 20,25, 30]
    R = [0.0,5, 10,15, 20,25,30]
    count = 0
    coordX = []
    coordY = []
    for r, t in rtpairs(R, T):
        cur_latitude = latitude + (r*np.cos(t))/6378000*(180/np.pi)
        cur_longitude = longitude + (r*np.sin(t))/6378000*(180/np.pi)/np.cos(latitude*np.pi/180)
        coordX.append(cur_latitude)
        coordY.append(cur_longitude)
        points_x.append(cur_latitude)
        points_y.append(cur_longitude)
        pointsStr += str(cur_latitude)+","+ str(cur_longitude) + "|"
        count = count + 1
        if(count % 50 == 0):
            pointsStr = pointsStr[:-1]
            lowest_elevation = getElevation(pointsStr, coordX, coordY, ax, lowest_elevation, points_z)
            coordX = []
            coordY = []
            pointsStr = ""
    #After finishing obtain all the points, clear the variables for getting next circles of points
    pointsStr = pointsStr[:-1]
    lowest_elevation = getElevation(pointsStr, coordX, coordY, ax, lowest_elevation, points_z)
    coordX = []
    coordY = []
    pointsStr = ""
    return lowest_elevation

def getPointsEvenlySmall(latitude, longitude, points_x, points_y, points_z):
    T = [1, 2,4,6,8,10]
    R = [0.0,2,4,6,8,10]
    count = 0
    coordX = []
    coordY = []
    pointsStr = ''
    for r, t in rtpairs(R, T):
        cur_latitude = latitude + (r*np.cos(t))/6378000*(180/np.pi)
        cur_longitude = longitude + (r*np.sin(t))/6378000*(180/np.pi)/np.cos(latitude*np.pi/180)
        coordX.append(cur_latitude)
        coordY.append(cur_longitude)
        points_x.append(cur_latitude)
        points_y.append(cur_longitude)
        pointsStr += str(cur_latitude)+","+ str(cur_longitude) + "|"
        count = count + 1
        if(count % 50 == 0):
            pointsStr = pointsStr[:-1]
            getElevation(pointsStr, coordX, coordY, ax, lowest_elevation, points_z)
            coordX = []
            coordY = []
            pointsStr = ""
    #After finishing obtain all the points, clear the variables for getting next circles of points
    pointsStr = pointsStr[:-1]
    getElevation(pointsStr, coordX, coordY, ax, lowest_elevation, points_z)
    coordX = []
    coordY = []
    pointsStr = ""
    return 


def calculateDistanceEachPath (points_x, points_y, index, ten_points):
    # now we have 5 possible points for z0, we need to search around these 5 points
    temp_x = []
    temp_y = []
    temp_z = []
    temp_latitude = points_x[index]
    temp_longitude = points_y[index]
    getPointsEvenlySmall(temp_latitude, temp_longitude, temp_x, temp_y, temp_z);
    distance_to_z1 = dict()
    distance_to_z2 = dict()
    distance_to_z3 = dict()
    distance_to_z4 = dict()
    for i in range(len(temp_z)):
        distance_to_z1[i] = abs(float(temp_z[i]) - float(ten_points[8]))
        distance_to_z2[i] = abs(float(temp_z[i]) - float(ten_points[7]))
        distance_to_z3[i] = abs(float(temp_z[i]) - float(ten_points[6]))
        distance_to_z4[i] = abs(float(temp_z[i]) - float(ten_points[5]))
    sorted_distance_to_z1 = sorted(distance_to_z1.items(), key=operator.itemgetter(1))
    sorted_distance_to_z2 = sorted(distance_to_z2.items(), key=operator.itemgetter(1))
    sorted_distance_to_z3 = sorted(distance_to_z3.items(), key=operator.itemgetter(1))
    sorted_distance_to_z4 = sorted(distance_to_z4.items(), key=operator.itemgetter(1))
    d_z1 =  map(operator.itemgetter(1), sorted_distance_to_z1[0:1])[0]
    d_z2 =  map(operator.itemgetter(1), sorted_distance_to_z2[0:1])[0]
    d_z3 =  map(operator.itemgetter(1), sorted_distance_to_z3[0:1])[0]
    d_z4 =  map(operator.itemgetter(1), sorted_distance_to_z4[0:1])[0]
    distance = d_z1 + d_z2 + d_z3 + d_z4
    return distance


#after obtaining three arrays points_x, points_y, and points_z, which are all the possible combination of
#longitude, latitude and elevation in the circle of radius 60m. We match the elevation points to find a 
#closest path.
def calculate_path (points_x, points_y, points_z, ten_points):
    #find 5 closest point to z0
    five_points_closest_to_z0 = dict()
    distance_to_z0 = dict()
    for i in range (len(points_z)):
        five_points_closest_to_z0[i] = points_z[i]
        distance_to_z0[i] = abs(float(points_z[i]) - float(ten_points[9]))
    sorted_distance_to_z0 = sorted(distance_to_z0.items(), key=operator.itemgetter(1))
    # print sorted_distance_to_z0[0:5] #(i, distance)
    z0_index_0 = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[0]
    z0_index_1 = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[1]
    z0_index_2 = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[2]
    z0_index_3 = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[3]
    z0_index_4 = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[4]
    distance_z0 = []
    distance_z0.append(calculateDistanceEachPath(points_x, points_y, z0_index_0,ten_points))
    # time.sleep(0.5) 
    distance_z0.append(calculateDistanceEachPath(points_x, points_y, z0_index_1,ten_points))
    # time.sleep(0.5) 
    distance_z0.append(calculateDistanceEachPath(points_x, points_y, z0_index_2,ten_points))
    # time.sleep(0.5) 
    distance_z0.append(calculateDistanceEachPath(points_x, points_y, z0_index_3,ten_points))
    # time.sleep(0.5) 
    distance_z0.append(calculateDistanceEachPath(points_x, points_y, z0_index_4,ten_points))
    lowest_distance = 1
    lowest_distance_index = 0;
    for i in range (5):
        if distance_z0[i] < lowest_distance:
            lowest_distance_index = i
    z0_index_final = map(operator.itemgetter(0), sorted_distance_to_z0[0:5])[lowest_distance_index]
    z0_final = []
    z0_final.append(points_x[z0_index_final])
    z0_final.append(points_y[z0_index_final])
    z0_final.append(points_z[z0_index_final])
    return z0_final





if __name__ == '__main__':

    # Collect the Latitude/Longitude input string
    # from the user
    # latitude = raw_input('Enter the latitude of your current location:   ')
    # if not latitude:
    #   latitude = 40.114637

    # longitude = raw_input('Enter the longitude of your current location:    ')
    # if not longitude:
    #   longitude = -88.228342

    pointsStr = ""
    #initialize 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    lowest_elevation = 1000
    zscale = 3
    ax.set_xlabel("latitude")
    ax.set_ylabel("longitude")
    ax.set_zlabel("elevation")

    pathLongitute = []
    pathLatitude = []
    pathElevation = []


    points_x = []
    points_y = []
    points_z = []
    
    path_final = []
    for i in range(len(Path_List)):
        #generate points_x, points_y, points_z arrays and add points to the graphs
        lowest_elevation = getPointsEvenly(float(Path_List[i][0]), float(Path_List[i][1]), pointsStr, points_x, points_y, points_z, lowest_elevation)
        path_final = calculate_path(points_x, points_y, points_z, Path_List[i][2:12])
        pathLongitute.append(path_final[0])
        pathLatitude.append(path_final[1])
        pathElevation.append(path_final[2])


    for i in range(len(pathLongitute)):
        ax.scatter(pathLatitude[i],pathLongitute[i], pathElevation[i], c='b', marker='o')
    
    # ax.set_zlim3d(lowest_elevation, lowest_elevation+zscale)
    # ax.set_xlim3d(40.08, 40.10)
    # ax.set_ylim3d(-88.2415, -88.2408)
    plt.show()    
