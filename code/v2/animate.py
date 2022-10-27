#!/usr/bin/env python3
import time, anim, sys
from pathlib2 import Path
from csv_load import *

description = """
Main script for running animations from csv files.
Change INPUT to the desired input file name.  
To install the required libraries do : 
    python -m pip install -r requirements.txt
"""

INPUT = 'Visually_Guided_Reaching_-_Child__4_target_-_LEFT_-_10_06.csv'

data_folder = Path("testfiles")
input_file = str(data_folder / INPUT)

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

        trial = Trial(dataframes[i], name = input_file[:-4] + "_T" + str(i), filter = None)  
        print(f"This trial duration is {trial.duration} seconds.")
        event_table(trial)
        
        # Plot of right hand v. left hand over time.
        anim.armspeed(trial, save=False, filename = trial.name)
        # Other plots
        anim.animate_gaze_double(trial, save=False, speed=20, filename=trial.name)                        
        # anim.animate_all(trial, plot=True, save=False, speed=10, filename=trial.name)
        
    print("Process finished in %s seconds." % round((time.time() - start_time),2))

if __name__ == "__main__":
    print(f"\nReading file: {input_file}", sep="")
    try: 
        main()
    except FileNotFoundError:
        print("Please enter a valid filename located in tesfiles folder")
        print(description)