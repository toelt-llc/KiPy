#!/usr/bin/env python3
import anim, os, time, sys, warnings
from csv_load import *
sys.path.append('./animations/')
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
# When ran on NaNs only arrays the medfilt function outputs NaNs

# Script used to process the 'flickering data' and visualize the data.
# The median filtering function is illustrated with the static and animation functions from the anim module

start_time = time.time()

# IMPORTANT 
# If you have all the files (13 CSVs) in your directory, use this code

# DIR = "../files/utf8_2/"
# FILES = []
# for root, dir, files in os.walk(DIR, topdown=False):
# #    print(os.path.abspath(os.getcwd()))
#     for file in sorted(files):
#         FILES.append(os.path.join(root, file))

# Otherwise, use this code:
visual1 = "../files/utf8_2/Visually_Guided_Reaching_-_Child__4_target_-_LEFT_-_10_06.csv"
visual2 = "../files/utf8_2/Visually_Guided_Reaching_-_Child__4_target_-_LEFT_-_10_07.csv"
FILES = [visual1, visual2]

#FILTERS = [7, 14]
for f in FILES:
    #filename = " " + f[16:]
    dfs = extract_dataframes(f, set=2)
    print("Processing file : ", f), print("Trials: ", len(dfs))
    for i in range(len(dfs)):
        trial = Trial(dfs[i], f, 14)
        #print(trial.duration)
        anim.animate_gaze_single_medfilt(trial, plot=False, save=False, speed=40, filename= f)#, filename=f[16:21]+str(14))
        #anim.static_gaze_single_medfilt(trial, plot=False, save=True, filename= f)# filename=f[16:21]+str(14))

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))