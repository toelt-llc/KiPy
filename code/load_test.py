from csv_load import *
import pandas as pd
import matplotlib.pyplot as plt

ball = "../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
object_hit = "../files/utf8/Object_Hit_-_Child_-_RIGHT_-_12_02.csv"

EXERCISE = ball

if EXERCISE[14] == 'B':
    dfs = extract_dataframes(EXERCISE, offset=6)
elif EXERCISE[14] == 'C':
    dfs = extract_dataframes(EXERCISE, offset=0)
elif EXERCISE[14] == 'O' or 'R' :
    dfs = extract_dataframes(EXERCISE, offset=3)

trial1 = Trial(dfs[0])



def plots(dic):
        fig = plt.figure()
        plt.plot(dic['right_x'],dic['right_y'],'ro', label='right')
        #plt.plot(dataframe['Left: Hand position X'],dataframe['Left: Hand position Y'],'bo', label='left')
        #plt.plot(dataframe['Gaze_X'],dataframe['Gaze_Y'],'go', label='gaze')
        plt.legend()
        plt.savefig("right_test.svg")
        plt.close(fig)
        #plt.show()
        #return fig 


plots(trial1.kinematics)