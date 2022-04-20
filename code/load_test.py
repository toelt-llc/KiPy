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


for i in range(len(dfs)):
    print(i)
    trial = Trial(dfs[i])
    print(trial.count)
    #plots(trial.kinematics)
    # title = str(i) + EXERCISE[14:17] + "right_test.png"
    # trial.plot_movements(title, save=False, show=True)
    #plt.show()         #Controls the plotting or not when running it, like plot=True
    # print(trial.events_cnt)
    # print(trial.events)
    title = str(i) + EXERCISE[14:17] + "anim.avi"
    print(trial.animate(title))

