#!/usr/bin/env python3
import time, sys, os
from csv_load import *
sys.path.append('./animations/')
import anim

# Script used to process the 'flickering data' and visualize the data.
# The median filtering function is illustrated with the static and animation functions from the anim module

start_time = time.time()

#practice_object = "../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"
#EXERCISE = practice_object
#dfs = extract_dataframes(EXERCISE)

DIR = "../files/utf8_2/"
FILES = []
for root, dir, files in os.walk(DIR, topdown=False):
#    print(os.path.abspath(os.getcwd()))
    for file in sorted(files):
        FILES.append(os.path.join(root, file))

FILTERS = [7, 14]
for f in FILES:
    filename = " " + f[16:]
    dfs = extract_dataframes(f, set=2)
    print("Processing file : ", f), print("Trials: ", len(dfs))
    for i in range(len(dfs)):
        #for s in FILTERS:
        trial = Trial(dfs[i], filename, 14)
        print(trial.duration)
        anim.animate_gaze_single_medfilt(trial, plot=False, save=True, speed=40, filename=f[16:21]+str(14))
        anim.static_gaze_single_medfilt(trial, plot=False, save=True, filename=f[16:21]+str(14))
    #plt.close()


print("Process finished -- %s seconds --" % round((time.time() - start_time),2))


