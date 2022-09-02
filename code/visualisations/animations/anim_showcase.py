import time, os, sys, inspect, warnings, pickle, blosc
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
codedir = os.path.dirname(os.path.dirname(currentdir))
#print(currentdir)
print(codedir)

sys.path.append(codedir)
import anim
from csv_load import *

start_time = time.time()

reaching = "../../../files/pickles/1/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.pickle"
reaching2 = "../../../files/pickles/1/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.pickle"
practice_ball = "../../../files/pickles/1/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.pickle"
ball = "../../../files/pickles/1/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.pickle"
practice_object = "../../../files/pickles/1/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.pickle"

EXERCISE = ball
with open(EXERCISE, "rb") as f:
    compressed_pickle = f.read()

dataframes = pickle.loads(blosc.decompress(compressed_pickle))
print("The input file contains {} trials.".format(len(dataframes)))

for i in range(len(dataframes)):
    trial = Trial(dataframes[i], EXERCISE[25:29] + str(i), filter=None)
    #print(trial.events) # Outputs the dic of events, with starting frame and starting second
    #print(trial.event_mean) #Outputs the mean of the events duration for the given trial, also computes std

    # print(i, trial.count, trial.duration, trial.rate)
    anim.armspeed(trial, save=False)
    anim.animate_gaze_single(trial, plot=True, save=False, speed=10)
    #anim.animate_gaze_triple(trial, plot=True, save=False, speed=20, filename=trial.name)
    #anim.animate_all(trial, plot=True, save=False, speed=10)

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))

# Command to convert the videos to gifs
#ffmpeg -i animation2_v3.mp4 -r 30 converted2.gif  