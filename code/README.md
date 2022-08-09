# Main python module directory

## Description

This core directory contains the programs and tests to analyse the CSV files and their trials.  
The directory contains the modules to automatically extract the data columns for each trial, for any task.
*Work In Progress* : Statistics module. 

## Getting Started

[Notebook Walkthrough](https://github.com/toelt-llc/gaze-kuleuven/blob/main/code/nb_walkthrough.ipynb) gets into the process of the csv reading and first visualisations.
The [second Notebook](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/blob/main/code/processing_flicker.ipynb) goes through the second part of this work where we try to filter and compute results out of flickering/missing raw data.      
Running an animation Example: see [Executing programs](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/code#executing-programs)

### Dependencies

Python ([Install python](https://www.python.org/downloads/)), with libraries:
- Required libraries: 
    - jupyterlab, pandas, numpy, matplotlib, pickle, blosc
    - From a python install do the following shell commands to install libraries:  
```bash
python -m pip install [library] 
# for example :
python -m pip install jupyterlab
```

## Data source: 
Stored in the [files](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/files) folder.  
**Note** due to the size of the files they can not be uploaded on GitHub, only the pre-processed and compressed (with pickle library) are available.  
Currently a single smaller file from a *Visually Guided Reaching* task is saved for each of the 2 datasets (normal and flickering), to be used as an example.  


The files are annoted large csv tables containing the kinematics informations from each experiments.  In the files the trials are individually separated.  Some experiments contain one single long trial (eg. the *Ball On Bar* exercise) and others contain several shorter trials.  A trial is considered as an individual attempt to complete one task.  Additionaly, the files also contain detailed experiments setup data. This data is removed during the pre-processing step in order to save only the dataframe containing the timed kinematics for a given trial.  

## Content

**Scripts & Notebooks** :   
>anim_showcase.py : script used to plot and save the animations from normal trial(s).  
>anim_showcase2.py : script used to process the 'flickering data' and visualize the data.  
>convert.sh : bash script to convert all CSVs to UTF8, used only once in the pre-processing.  
>csv_load.py : contains the python class to extract the trials from a CSV file .   
>preprocessing.ipynb : first notebook and attempts at reading the CSVs files.  

*Note*: the flickers can be observed as coming from missing values in the gaze X&Y columns, this is noted in:  
>processing_flicker.ipynb: notebook for the exploration of flickering CSVs.  

**Directories**  
-[Animations](https://github.com/toelt-llc/gaze-kuleuven/tree/main/code/animations):  
Contains the animation modules and useful functions. Animations saved from the *anim_showcase* scripts are saved here in subfolders.  
-[Images](https://github.com/toelt-llc/gaze-kuleuven/tree/main/code/images)  
Contains visualizations for differents parameters. Images are also obtained from the scripts.  


### Executing programs

* Running the [Notebook Walkthrough](https://github.com/toelt-llc/gaze-kuleuven/blob/main/code/nb_walkthrough.ipynb) helps to understand the steps involved, from the CSV files reading to the animations and extraction of parameters.   

* Running the animations script
```bash
> python3 anim_showcase.py
> python3 anim_showcase2.py
```

These scripts are made to be manually changed depending on which visualisation is needed, it is possible to set it to plot or save the animations thanks to functions like the following:   
```python 
anim.animate_gaze_single(trial, plot=True, save=True, filename='[video_name]',speed = 10)
```
*plot* : True: open animation visualisation, False: don't open  
*save*: True: save the animation as a mp4 video under code/animations/[filename]   
*speed* parameter regulates the frame rate of the animation, and the total video length; default is 1.  

### *anim_showcase.py*
Lines 23 to 26 contain commented functions which the user can run and modify to either plot and/or save animations and plots: 
- **anim.armspeed()**: plots the arms speed over time for each trial contained in the input file
- **anim.animate_gaze_single()**: plots animation of the gaze for each trial
- **anim.animate_gaze_triple()**: plots the same animation but with 1:gaze position 2: gaze position + history 3: full position history
- **anim.animate_all()**: plots the triple animation and includes the hand positions.

### *anim_showcase2.py*
Similar idea than the previous script, the goal here is to visualise the effects of some filtering attempts on flickering data(the 2nd dataset).  
- **anim.animate_gaze_single_medfilt()**: plots animation of the data filtered data compared to the raw flickering data
- **anim.static_gaze_single_medfilt()**: plots static position history of the filtered vs raw
