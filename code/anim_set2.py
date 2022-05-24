#!/usr/bin/env python3
import time, sys, os
from csv_load import *
sys.path.append('./animations/')
import anim

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

FILTERS = [90, 150, 500]
for f in FILES[:9]:
    filename = " " + f[16:]
    dfs = extract_dataframes(f, set=2)
    print(len(dfs), f)
    for i in range(len(dfs)):
        trial = Trial(dfs[i], filename)
        print(trial.duration)
        for s in FILTERS:
            anim.animate_gaze_single_medfilt(trial, plot=False, save=True, filter=s, speed=10, filename=f[16:20]+str(s))
    #plt.close()


print("Process finished -- %s seconds --" % round((time.time() - start_time),2))