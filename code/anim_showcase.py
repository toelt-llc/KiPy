#!/usr/bin/env python3
import sys
sys.path.append('./animations/')
from csv_load import *
from anim import *

reaching = "../files/utf8/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.csv"
#reaching2 = "../files/utf8/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.csv"
practice_ball = "../files/utf8/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv"
ball = "../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
practice_object = "../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"

EXERCISE = practice_object

if EXERCISE[14] == 'B':
    dfs = extract_dataframes(EXERCISE, offset=6)
elif EXERCISE[14] == 'C':
    dfs = extract_dataframes(EXERCISE, offset=0)
elif EXERCISE[14] == 'O' or 'R' :
    dfs = extract_dataframes(EXERCISE, offset=3)

for i in range(len(dfs)):
    trial = Trial(dfs[i])
    print(i, trial.count, trial.duration, trial.rate)
    #animate_gaze_single(trial, save=False)
    #animate_gaze_triple(trial, save=False)
    animate2(trial, save=True)

