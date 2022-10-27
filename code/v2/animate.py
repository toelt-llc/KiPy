#!/usr/bin/env python3
import time, anim, sys
from pathlib2 import Path
from csv_load import *

description = """
"""

INPUT = 'Ball_on_Bar_-_Child_-_RIGHT_-_10_21.csv'

data_folder = Path("testfiles")
input_file = data_folder / INPUT
print(input_file.name)
input_file = str(input_file)

if len(sys.argv) == 1:
    input_file = input_file
elif len(sys.argv) > 1:
    input_file = sys.argv[1]

def main():
    start_time = time.time()

    dataframes = extract_dataframes(input_file)
    for i in range(len(dataframes)):                                     
        print(f"Processing trial {i+1} of {len(dataframes)}.")
        print(20*'=')

        trial = Trial(dataframes[i], name = input_file + str(i), filter = None)      
        print(f"This trial duration is {trial.duration} seconds.")
        event_table(trial)
        
        # Plot of right hand v. left hand over time.
        anim.armspeed(trial, save=False, filename = trial.name)
        anim.animate_gaze_double(trial, save=False, speed=20, filename=trial.name)                                       
        # # Create a video animation from the gaze data. 
        #anim.animate_gaze_single(trial, plot=False, save=True, speed=40, filename=trial.name)  
        # # Create a triple animation, similar to the gaze triple and includes hands positions. 
        # anim.animate_all(trial, plot=True, save=False, speed=10, filename=trial.name)
        

    print("Process finished -- %s seconds --" % round((time.time() - start_time),2))

if __name__ == "__main__":
    print(f"Reading file: {input_file}")
    main()