#!/usr/bin/env python3
import time, os, sys, inspect, warnings, pickle, blosc
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
codedir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(codedir)
import anim
from csv_load import *
# NB: When ran on NaNs only arrays the medfilt function outputs NaNs

# Script used to process the 'flickering data' and visualize the data.
# The median filtering function is illustrated with the static and animation functions from the anim module

DIR = "../../../files/pickles/2/"
#if my_os: DIR = path_replace(DIR)
FILES = []
for root, dir, files in os.walk(DIR, topdown=False):
#    print(os.path.abspath(os.getcwd()))
    for file in sorted(files):
        FILES.append(os.path.join(root, file))

start_time = time.time()

FILTERSIZE = 14     #Example filter size to compare

for f in FILES[2:3]: #Only display the chosen example, can be changed
    with open(f, "rb") as f:
        compressed_pickle = f.read()
    dfs = pickle.loads(blosc.decompress(compressed_pickle))
    print("Processing file : ", f.name), print("Trials: ", len(dfs))
    for i in range(len(dfs)):
        trial = Trial(dfs[i], f.name[25:], FILTERSIZE)
        #print(trial.duration)
        anim.animate_gaze_single_medfilt(trial, plot=True, save=False, speed=40, filename= f)#, filename=f[16:21]+str(14))
        #anim.static_gaze_single_medfilt(trial, plot=True, save=False, filename= f)# filename=f[16:21]+str(14))

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))