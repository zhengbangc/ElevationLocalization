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

# Obtain data from csv file
Path_CSV = open("paths/07-41-16_12:41:24_MSFINAL.csv")
CSV_Reader = csv.reader(Path_CSV)
Path_List = list(CSV_Reader) #the third column are elevations
print len(Path_List)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
lowest_elevation = 1000
zscale = 3
ax.set_xlabel("latitude")
ax.set_ylabel("longitute")
ax.set_zlabel("elevation")

for i in range(len(Path_List)):
	ax.scatter(float(Path_List[i][1]), float(Path_List[i][0]), float(Path_List[i][11]), c='b', marker='o')

# ax.set_zlim3d(lowest_elevation, lowest_elevation+zscale)
# ax.set_xlim3d(40.08, 40.10)
# ax.set_ylim3d(-88.2415, -88.2408)
plt.show()