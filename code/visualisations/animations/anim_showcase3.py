#!/usr/bin/env python3
import time, os, sys, inspect, warnings, pickle, blosc
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
codedir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(codedir)
import anim
from csv_load import *
# anim_showcase complete list, from paper appendix
start_time = time.time()

reaching = "../../../files/pickles/1/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.pickle"
reaching2 = "../../../files/pickles/1/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.pickle"
practice_ball = "../../../files/pickles/1/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.pickle"
ball = "../../../files/pickles/1/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.pickle"
practice_object = "../../../files/pickles/1/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.pickle"

#EXERCISE = '<source file location>'
#dataframes = extract_dataframes(EXERCISE)
EXERCISE = ball
with open(EXERCISE, "rb") as f:
    compressed_pickle = f.read()

dataframes = pickle.loads(blosc.decompress(compressed_pickle))
print("The input file contains {} trials.".format(len(dataframes)))

for i in range(len(dataframes)):                                            # For each trial contained in the source file.
    trial = Trial(dataframes[i], name = EXERCISE[25:29] + str(i), filter = None)
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