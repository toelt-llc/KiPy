# KiPy - Software to extract hands and eye-gaze coordinates from Kinarm Files

Author: Arnaud Gucciardi, (C) 2022 A. Gucciardi

This repository contains the KiPy software. The software is described in the paper, along with the eperimental setup:

_A New Median Filter Application to Deal with Large Windows of Missing Data in Eye-gaze Measurements_ (2022)
Arnaud Gucciardi, Monica Crotti, Nofar Ben Itzhak, Lisa Mailleux, Els Ortibus, Umberto Michelucci, Vida Groznik and Alexander Sadikov.

In case you use it a reference to this paper will be nice.



# Background

The software helps assessing cerebral palsy and other possible brain damages in children aged 7 to 15, thanks to a non-invasive tool.  
The technical tool ([Kinarm exoskeleton lab](https://kinarm.com/kinarm-products/kinarm-exoskeleton-lab/)) used in the clinical experiments is not presented here. 
The software focuses on the analysis of output files and results.   
Research Objectives :  
1. Visual functions assessment.  
2. Visual impact on manual control -> from the **task experiments**.  
3. MRI data coupling: structural visualization.  

This software is the basis for the 3 tasks.

# Brief Description

We use data extracted from the Kinarm software as CSV files.  4 different types of files are available, from the 4 different experimental tasks.  
The goal is to extract the experiments measurements from these files. Then, from the measures we study what is possible to obtain in terms of statistics and graphical representation.  
The statistics on the measure can be further used for the analysis of evaluation parameters, linked to the research questions.  

***Figure 1: Representation example***  
![Whole anim](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/blob/main/code/visualisations/animations/final/convertedall.gif) 

# Concept
In our part of the project we focus on the reading of the csv files: what can we extract that the software does not produces.  
<!-- With the research problematics in head  -->
To produce visualisations and to compute statistic we (mainly) need to access both the hand positions data and the gaze tracking data. 

<!--## Results  
*What was down with the raw CSVs and what can we learn from them.*   

- We extracted the dataframes : 1 dataframe = 1 exercise trial (learned how to extract differently for each exercise)  
    - Each new CSV result file can be processed with the functions built from what was learned on the first files. (*csv_load.py*)  
- One dataframe contain all the information related to a single **trial**.  Each row of a dataframe contains the information for a given moment. The rows are separated by 1ms each (corresponding to the eye tracker track-rate).  
    - Data columns for each rows can be separated in 2 categories: 
        - Kinematics: the positions, angles and speeds.  
        - Events: If an event happens at a given frame, it will be noted in the according row.  
-->
## Running the code

To run the code a basic installation of python is needed, further details are in the [Code Readme](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/code#readme)

## Repository content
### code 
Contains:
- walkthrough (and experimental) notebooks & scripts, detailed in the [Code Readme](https://github.com/toelt-llc/RESEARCH-gaze-kuleuven/tree/main/code#readme).
- **bash_scripts**, pre-processing scripts used during csv exploration. 
- **animations**, animation module and examples of possible animations of gaze/hands data.  (See example above.)  
- **images**, possibles plots of gaze/hands data.
### docs
Explanatory documents from Monica Crotti, with additional Kinarm matlab sources, documentation and presentations.
### files
CSV files storage, important for the path variable used in code.  
Subfolders:  
- *set1*, *set2*   : original CSVs in raw format (ISO-8859).  
- *utf8*, *utf8_2* : UTF8-converted CSV files. 

-- Documentation version: 08/2022 --
