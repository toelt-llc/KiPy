#!/usr/bin/env python3
import time, sys, warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
sys.path.append('../../')
import anim
from csv_load import *
# TODO: Use the compressed pickles instead of the raw CSV
# anim_showcase complete list, from paper appendix
start_time = time.time()

reaching = "../../../files/utf8/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.csv"
reaching2 = "../../../files/utf8/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.csv"
practice_ball = "../../../files/utf8/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv"
ball = "../../../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
practice_object = "../../../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"

#EXERCISE = '<source file location>'
EXERCISE = ball
dataframes = extract_dataframes(EXERCISE)
print("The input file contains {} trials.".format(len(dataframes)))

for i in range(len(dataframes)):                                            # For each trial contained in the source file.
    trial = Trial(dataframes[i], name = EXERCISE + str(i), filter = None)
    #print(trial.events)                                                     # Outputs the dictionnary of events, with starting frame and starting second.
    #print(trial.event_mean)                                                 # Outputs the mean of the events duration for the given trial, also computes std.

    print("Dataframe number : {}, the trial duration is {}".format(i, trial.duration))
    # Functions 

    # Plot of right hand v. left hand over time.
    anim.armspeed(trial, filename = trial.name, save=False)                                            
    # Create a video animation from the gaze data. 
    anim.animate_gaze_single(trial, plot=True, save=False, speed=10, filename=trial.name)  
    # Create a triple frame video animation: 1)gaze position 2)gaze position tracing 3)full position history.
    anim.animate_gaze_triple(trial, plot=True, save=False, speed=10, filename=trial.name)
    # Create a triple animation, similar to the gaze triple and includes hands positions. 
    anim.animate_all(trial, plot=True, save=False, speed=10, filename=trial.name)

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))

# Command to convert the videos to gifs
#ffmpeg -i animation2_v3.mp4 -r 30 converted2.gif  