# Main python/ipynb code directory

## Description

In this core repository we have the programs and tests to analyse the CSV files and their trials.
Contains the modules to automatically extract the data columns for each trial, for any task.
*TODO* : Statistics module. 

# Getting Started

[Notebook Walkthrough](https://github.com/toelt-llc/gaze-kuleuven/blob/main/code/nb_walkthrough.ipynb)  
[Running an animation Example]: see 'Executing programs'

### Dependencies

* Python, with libraries:  
 -Jupyterlab, Pandas, Numpy, Matplotlib

## Content


**Scripts & Notebooks** :   
>anim_showcase.py : script used to plot and save the animations from normal trial(s).  
>anim_showcase2.py : script used to process the 'flickering data' and visualize the data.  
>convert.sh : bash script to convert all CSVs to UTF8, used in the pre-processing.  
>csv_load.py : contains the python class to extract the trials from a CSV.   
>preprocessing.ipynb : first notebook and attempts at reading the CSVs.  

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
```
> python3 anim_showcase.py
>
> python3 anim_showcase2.py
```

This script is made to be manually changed depending on what is needed, it is possible to set it to plot or save the animations thanks to functions like the following:   
``` 
anim.animate_gaze_single(trial, plot=True, save=True, filename='[video_name]',speed = 10)
```
The *speed* parameter regulates the frame rate of the animation, and the total video length.    
Lines 21 to 24 contain commented functions that can the user can run and modify to either plot or save (or both) animations and plots.  
