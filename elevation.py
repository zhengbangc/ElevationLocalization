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
    T = [1,2,4,6, 8,10, 12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96]
    R = [0.0,5,10,15, 20,25, 30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,185,180,195,200,205,210,215,220,225,230,235,240,245,250]
    for i in range(len(T)):
        T[i] = 10*T[i]

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

#find 5 closest point index to zx
def calculteClosest5points (points_z, ten_points, zx):
    distance_to_zx = dict()
    for i in range(len(points_z)):
        distance_to_zx[i] = abs(float(points_z[i]) - float(ten_points[zx]))
    sorted_distance_to_zx = sorted(distance_to_zx.items(), key=operator.itemgetter(1))
    closest_to_zx_idx = []
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[0])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[1])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[2])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[3])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[4])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[5])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[6])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[7])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[8])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[9])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[10])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[11])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[12])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[13])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[14])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[15])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[16])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[17])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[18])
    closest_to_zx_idx.append(map(operator.itemgetter(0), sorted_distance_to_zx[0:20])[19])

    return closest_to_zx_idx


# Add 10 values to final_path per call
def calculate_path (points_x, points_y, points_z, final_path, ten_points):
    points_pool_50 = []
    for i in range(10):
        points_pool_50.append(calculteClosest5points(points_z,ten_points,i))
    #now we have 5 possible location for each of the 10 sample points
    #we need to figure out a path with smallest length
    
    path_idices_arrays = []
    path_len_arrays = []
    path_idices = []
    path_len = 0
    distanceSquare = dict()
    #calculate the distance between the current point and the next 5 points
    for i in range(20):
        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[0][i]]-points_x[points_pool_50[1][j]])**2 + (points_y[points_pool_50[0][i]]-points_y[points_pool_50[1][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[1][closest_j]]-points_x[points_pool_50[2][j]])**2 + (points_y[points_pool_50[1][closest_j]]-points_y[points_pool_50[2][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[2][closest_j]]-points_x[points_pool_50[3][j]])**2 + (points_y[points_pool_50[2][closest_j]]-points_y[points_pool_50[3][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[3][closest_j]]-points_x[points_pool_50[4][j]])**2 + (points_y[points_pool_50[3][closest_j]]-points_y[points_pool_50[4][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[4][closest_j]]-points_x[points_pool_50[5][j]])**2 + (points_y[points_pool_50[4][closest_j]]-points_y[points_pool_50[5][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[5][closest_j]]-points_x[points_pool_50[6][j]])**2 + (points_y[points_pool_50[5][closest_j]]-points_y[points_pool_50[6][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[6][closest_j]]-points_x[points_pool_50[7][j]])**2 + (points_y[points_pool_50[6][closest_j]]-points_y[points_pool_50[7][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[7][closest_j]]-points_x[points_pool_50[8][j]])**2 + (points_y[points_pool_50[7][closest_j]]-points_y[points_pool_50[8][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()

        for j in range(20):
            distanceSquare[j]=(points_x[points_pool_50[8][closest_j]]-points_x[points_pool_50[9][j]])**2 + (points_y[points_pool_50[8][closest_j]]-points_y[points_pool_50[9][j]])**2
        sorted_distanceSqaure = sorted(distanceSquare.items(), key=operator.itemgetter(1))
        closest_j = map(operator.itemgetter(0), sorted_distanceSqaure)[0]
        path_idices.append(closest_j)
        path_len += map(operator.itemgetter(0), sorted_distanceSqaure)[1]
        distanceSquare.clear()
        
        # print path_idices
        # print path_len
        path_idices_arrays.append(path_idices)
        path_len_arrays.append(path_len)
        path_idices = []
        path_len = 0
    
    path_indices = []
    path_indices.append(path_len_arrays.index(min(path_len_arrays)))
    path_indices= path_indices + path_idices_arrays[path_len_arrays.index(min(path_len_arrays))]
    # print path_indices

    for i in range(10):
        final_path.append(points_pool_50[i][path_indices[i]])
    # print points_pool_50
    # print final_path



    return

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
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_zlabel("elevation")

    points_x = []
    points_y = []
    points_z = []
    lowest_elevation = getPointsEvenly(float(Path_List[len(Path_List)/2][0]), float(Path_List[len(Path_List)/2][1]), pointsStr, points_x, points_y, points_z, lowest_elevation);
    print len(points_x)
    print len(points_y)
    print len(points_z)

    csvOutputArray = []
    for i in range(len(points_x)):
        # ax.scatter(points_x[i],points_y[i], points_z[i], c='b', marker='o')
        csvOutputArray.append([points_x[i], points_y[i],points_z[i]])

    #Output the large circle into a csv
    with open('mydata.csv', 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile, dialect='excel')
        for row in csvOutputArray:
            thedatawriter.writerow(row)

    # Final path will contain len(Path_List)*10 values, each specifies the index of points in points_x, points_y and points_z array
    final_path = []
    for i in range(len(Path_List)):
        calculate_path(points_x, points_y, points_z, final_path, Path_List[i][2:12])
    # print final_path

    for i in range(len(final_path)):
        ax.scatter(points_x[final_path[i]],points_y[final_path[i]], points_z[final_path[i]], c='b', marker='o')


    # for i in range(len(pathLongitute)):
    #     ax.scatter(pathLatitude[i],pathLongitute[i], pathElevation[i], c='b', marker='o')
    
    # ax.set_zlim3d(lowest_elevation, lowest_elevation+zscale)
    # ax.set_xlim3d(40.08, 40.10)
    # ax.set_ylim3d(-88.2415, -88.2408)
    plt.show()    
