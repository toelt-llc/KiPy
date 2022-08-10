#!/usr/bin/env python3
import sys, time
sys.path.append('../../')
import anim
from csv_load import *
# TODO: Use the compressed pickles instead of the raw CSV
start_time = time.time()

reaching = "../../../files/utf8/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.csv"
reaching2 = "../../../files/utf8/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.csv"
practice_ball = "../../../files/utf8/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv"
ball = "../../../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
practice_object = "../../../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"

EXERCISE = reaching
dfs = extract_dataframes(EXERCISE)
print("The input file contains {} trials.".format(len(dfs)))

for i in range(len(dfs)):
    trial = Trial(dfs[i], EXERCISE[20:29] + str(i), filter=None)
    #print(trial.events) # Outputs the dic of events, with starting frame and starting second
    #print(trial.event_mean) #Outputs the mean of the events duration for the given trial, also computes std

    # print(i, trial.count, trial.duration, trial.rate)
    anim.armspeed(trial, filename=trial.name)
    anim.animate_gaze_single(trial, plot=True, save=False, speed=10, filename=trial.name)
    #anim.animate_gaze_triple(trial, plot=True, save=False, speed=20, filename=trial.name)
    #anim.animate_all(trial, plot=True, save=False, speed=10)

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))

# Command to convert the videos to gifs
#ffmpeg -i animation2_v3.mp4 -r 30 converted2.gif  