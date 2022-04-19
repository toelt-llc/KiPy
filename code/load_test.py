from csv_load import *
import pandas as pd
import matplotlib.pyplot as plt

ball = "../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
object_hit = "../files/utf8/Object_Hit_-_Child_-_RIGHT_-_12_02.csv"
# practice example is from ball_on_bar exercise
practice_ball = "../files/utf8/Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv"
practice_object = "../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"
circuit = "../files/utf8/Circuit_Exo_-_[b_Circuit1_(youngerchildren)]_-_RIGHT_-_12_09.csv"
reaching = "../files/utf8/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.csv"


EXERCISE = ball

if EXERCISE[14] == 'B':
    dfs = extract_dataframes(EXERCISE, offset=6)
elif EXERCISE[14] == 'C':
    dfs = extract_dataframes(EXERCISE, offset=0)
elif EXERCISE[14] == 'O' or 'R' :
    dfs = extract_dataframes(EXERCISE, offset=3)


#print(type(trial1.kinematics['right_x'][0]))


def plots(dic):
        fig = plt.figure()
        #plt.plot(dic['right_x'],dic['right_y'],'ro', label='right')
        floatx = [float(i) for i in dic['right_x']]
        floaty = [float(i) for i in dic['right_y']]
        plt.plot(floatx, floaty,'ro', label='right')
        #plt.plot(dataframe['Left: Hand position X'],dataframe['Left: Hand position Y'],'bo', label='left')
        #plt.plot(dataframe['Gaze_X'],dataframe['Gaze_Y'],'go', label='gaze')
        plt.legend()
        #plt.savefig("right_test.svg")
        #plt.close(fig)
        plt.show()
        #return fig 

for i in range(len(dfs)):
    print(i)
    trial = Trial(dfs[i])
    print(trial.count)
    #plots(trial.kinematics)
    title = str(i) + EXERCISE[14:17] + "right_test.png"
    trial.plots(title)