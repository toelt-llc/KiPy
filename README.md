# Gaze-kuleuven

<Landing page : Here need to identify purpose of the folder, as well as an introduction>

This folder contains the data processing exploration from the project shared with KU Leuven.  
The project assesses cerebral palsy and other possible brain damages in children aged 7 to 15, thanks to a non-invasive tool.  
Research Ojectives :  
-1 Visual functions assessment.  
-2 Visual impact on manual control -> from the **task experiments**.  
-3 MRI data coupling: structural visualization.  

Here we focus on 1,2.   
We use data extracted from the Kinarm software as CSV files.   4 different type of tasks are available.  
The goal is to extract the experiments measurements from these files. Then, from the measures we study what is possible to obtain in terms of statistics and graphical representation.  
The statistics on the measure can be further used for the analysis of evaluation parameters, linked to the research questions.  

***Figure : Representation example***  
![Whole anim](https://github.com/toelt-llc/gaze-kuleuven/blob/main/code/animations/final/convertedall.gif) 

# Concept
In our part of the project we focus on the reading of the csv files: what can we extract that the software does not produces.  
<!-- With the research problematics in head  -->
To produce visualisations and to compute statistic we need to access both the hand positions data and the gaze tracking data. 

## Results  
*What was down with the raw CSVs and what can we learn from them.*   

- We extracted the dataframes : 1 dataframe = 1 exercise trial (learned how to extract differently for each exercise)  
    - Each new CSV result file can be processed with the functions built from what was learned on the first files. (*csv_load.py*)  
- One dataframe contain all the information related to a single **trial**.  Each row of a dataframe contains the information for a given moment. The rows are separated by 1ms each (corresponding to the eye tracker track-rate).  
    - Data columns for each rows can be separated in 2 categories: 
        - Kinematics: the positions, angles and speeds.  
        - Events: If an event happens at a given frame, it will be noted in the according row.  

## Running the code

To run the code a basic installation of python is needed, further details are in the [Code readme](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/code#readme)

### Walkthrough file (move to code/README.md ?)
This [notebook](https://github.com/toelt-llc/gaze-kuleuven/blob/main/code/nb_walkthrough.ipynb) contains an overview of what was done at first, without getting deep in the python code.  
The [second notebook](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/blob/main/code/processing_flicker.ipynb) goes through the second part of this work where we try to filter and compute results out of flickering data.  
## Content
### code 
Contains:
- walkthrough (and experimental) notebooks & scripts, detailed in the [Code readme](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/code#readme).
- **animations**, possible animations of gaze/hands data.  
See example above.  
- **bash_scripts**, pre-processing scripts used during csv exploration. 
- **images**, possibles plots of gaze/hands data.
### docs
Explanatory documents from Monica, with kinarm matlab sources, documentation and presentations.
### files
Folder where the csv are stored, important for the path variable used in code.  
Subfolders:  
- *set1*, *set2*   : original CSVs in raw format (ISO-8859)
- *utf8*, *utf8_2* : converted CSV files 

-- Documentation version: 05/2022 --
