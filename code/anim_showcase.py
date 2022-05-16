#!/usr/bin/env python3
import sys
sys.path.append('./animations/')
from csv_load import *
import anim

reaching = "../files/utf8/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.csv"
reaching2 = "../files/utf8/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.csv"
practice_ball = "../files/utf8/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv"
ball = "../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
practice_object = "../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"

EXERCISE = practice_object
dfs = extract_dataframes(EXERCISE)

for i in range(1):
    trial = Trial(dfs[i])
    #print(trial.events)
    print(i, trial.count, trial.duration, trial.rate)
    print(trial.event_mean)
    #anim.armspeed(trial)
    #anim.animate_gaze_single(trial, plot=True, save=False, speed=10, filename=('ball_single'+str(i)))
    anim.animate_gaze_triple(trial, plot=True, save=False, speed=20, filename=('balltriple_s'+str(i)))
    #anim.animate_all(trial, save=True, plot=False, speed=2)


#ffmpeg -i animation2_v3.mp4 -r 30 converted2.gif  