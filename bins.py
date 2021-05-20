import glob
import os
import statistics
import time

import pandas as pd
from sortedcontainers import SortedList

start_time = time.time()
bins = {}
scanDict = {}
scanMassList = []
binsList = SortedList()
missing_values_dict = {}

# Scan multiple CSV files into a list of lists


# Each bin is inside of a bin dictionary.
# Define a bin which is 10 ppm on either side of a mass.
# A bin contains a key of masses with a list of them as values.
# Key of 'scan' and list of scans associated with the mass list
# Key of both the left and right edge with the calculated value
# The parameters are d=bins, x=the mass, i=the scan name, s=the standard deviation, l= left edge calculation, and r= right edge calculation
def new_bin(d, x, i):
    s = (10 / 1000000) * x
    l = x - s
    r = x + s
    masses = [x]
    i = [i]
    d[x] = {'masses': masses, 'scans': i, 'leftEdge': l, 'rightEdge': r, 'standardDeviation': 0, 'mean': None}


# When we are not creating a new bin, we need to update the bins with only the mass and the scan it came from.
# Right and left edges do not need to change
# The parameters are d=dictionary which is bins, i=the mass that the original bin was made from, x=the mass that is currently being evaluated, and s= the scan the current mass is from
def update_bin(d, i, x, s):
    if s in d[i]['scans']:
        new_bin(d, x, s)
    else:
        d[i]['masses'].append(x)
        d[i]['scans'].append(s)


# This is the key algorithm for finding where a mass resides
# The function takes d= dictionary, k=the key, v=value(usually the key as well), and s= the scan
def insertMass(d, k, v, s):
    # We want to see if our temporary bins list, which is a list of the masses that have already been assigned bins in the current scan, contains the current mass already.
    # If it does then we need to make a new bin, because no two masses from the same scan can reside in the same bin
    if tempBinsList.__contains__(v):
        new_bin(d, k, s)
    elif v == d.get(v):
        update_bin(d, v, v, s)
    else:
        # O log n
        # By adding the mass to a list of bins that is sorted using the Sorted Containers import we can get the indexes it falls between
        binsList.add(v)
        # O log n
        new_key_index = binsList.index(v)
        # With the indices to the left and right we can now see if our current mass satisfies the criteria to go into an already created bin, or we can create a new one if not
        left_ind = new_key_index - 1
        right_ind = new_key_index + 1
        try:
            # We look up the edges of the left and right bins and using comparison operators we can see if it falls in either the left bin or the right bin for placement
            left_compare = (binsList[left_ind])
            left_left_edge = bins[left_compare]['leftEdge']
            left_right_edge = bins[left_compare]['rightEdge']
            right_compare = (binsList[right_ind])
            right_left_edge = bins[right_compare]['leftEdge']
            right_right_edge = bins[right_compare]['rightEdge']
            if left_left_edge <= k <= left_right_edge:
                update_bin(d, left_compare, v, s)
                # By using a temporary bins dictionary we can remove the bin that a mass has been added to, this will ensure we don't add two masses from the same scan to the same bin
                tempBins.pop(v)
            elif right_left_edge <= k <= right_right_edge:
                update_bin(d, right_compare, v, s)
                tempBins.pop(v)
            else:
                new_bin(d, k, s)
        except (IndexError, KeyError):
            new_bin(d, k, s)


# This is our path to the files we are using. Each file is a scan consisting of Masses = M/Z and Intensities
path = os.path.join('/Users/taylorjanoe/PycharmProjects/Capstone/CSV/')

# We want to initialize the loop at 0 and increment, for the first scan we are always going to have to create a new bin for all elements.
loop = 0
# For each filename in the path
for fname in glob.glob(path + '*.csv'):
    # Creating a dataframe in order to execute or core algorithm
    df = pd.read_csv(fname, index_col=None, header=0)
    # Retrieving the file name of the scan which will be used in the bins and scan dictionary for look up in the main file
    scanName = os.path.basename(fname)
    # Reporting which files have missing values
    if df.isnull:
        a = df.isnull().sum()
        missing_values_dict[scanName] = a
    df.dropna(inplace=True)
    # Sorting the dataframe by intensity
    ordered_df = df.sort_values(by='Intensity')

    # Each scan becomes a dictionary used in the main to see mass and intensity
    scan_dict = scanDict.setdefault(scanName, df.to_dict('list'))
    # Creating a sorted list of masses that will be used in the insert_mass function
    tempBinsList = SortedList()
    tempBins = bins.copy()
    loop = loop + 1
    for v in df['M/Z']:
        # for the first scan every element needs to go into a new bin, "loop" is a counter and after the first one it moves to the else conditional statement
        if loop == 1:
            new_bin(bins, v, scanName)
            binsList.add(v)
        else:
            insertMass(bins, v, v, scanName)
            tempBinsList.add(v)
            binsList.add(v)


for key in bins:
    if len(bins[key]['masses']) >= 2:
        sl = bins[key]['masses']
        sd = statistics.stdev(sl)
        bins[key]['standardDeviation'] = sd
        mean = bins[key]['masses']
        mc = statistics.mean(mean)
        bins[key]['mean'] = mc
    else:
        pass

end_time = time.time()
print("Total execution time: {} seconds".format(end_time - start_time))
