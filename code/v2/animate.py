#!/usr/bin/env python3
import time, anim, sys, tabulate
from pathlib2 import Path
from csv_load import *

description = """
Main script for running animations from csv files.
Change INPUT to the desired input file name.  
To install the required libraries do : 
    python -m pip install -r requirements.txt
"""

INPUT = 'Ball_on_Bar_-_Child_-_RIGHT_-_10_21.csv'
CHILD_NAME = 'child0'

data_folder = Path("testfiles")
input_file = str(data_folder / INPUT)
columns_recap = ['Saccades N', 'Saccades Mean (s)', 'Saccades Std (s)', 
                 'Fixations', 'Fixations Mean (s)', 'Fixations Std (s)', 
                 'Blinks', 'Blinks Mean (s)', 'Blinks Std (s)']

if len(sys.argv) == 1:
    input_file = input_file
elif len(sys.argv) > 1:
    input_file = sys.argv[1]

def main():
    start_time = time.time()

    dataframes = extract_dataframes(input_file)
    df = pd.DataFrame(columns=columns_recap) 
    for i in range(len(dataframes)):           
        trial = Trial(dataframes[i], name = input_file[:-4] + "_T" + str(i), filter = None)  
        print(f"Processing trial {i+1} of {len(dataframes)}.")
        print(20*'=')
        print(f"Trial duration: {trial.duration} seconds.")

        df = event_table(CHILD_NAME, trial, i, df)

        # Plot of right hand v. left hand over time.
        #anim.armspeed(trial, save=False, filename = trial.name)
        # Other plots
        anim.animate_gaze_double(trial, save=False, speed=200, filename=trial.name)                        
        # anim.animate_all(trial, plot=True, save=False, speed=10, filename=trial.name)
    
    print("Dataframe saved: \n", tabulate.tabulate(df, headers='keys', tablefmt='fancy_outline', showindex=True), sep="")         
    df.to_csv(f"{CHILD_NAME}_{switch(INPUT)}.csv")
    print("Process finished in %s seconds." % round((time.time() - start_time),2))
    
if __name__ == "__main__":  
    print(f"\nReading file: {input_file}", sep="")
    try: 
        main()
    except FileNotFoundError:
        print("File not found! Enter a valid filename located in code/v2/testfiles")