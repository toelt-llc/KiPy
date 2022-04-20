from csv_load import *


reaching = "../files/utf8/Visually_Guided_Reaching_-_[Child_v2_-_practice]_-_LEFT_-_11_49.csv"

EXERCISE = reaching

if EXERCISE[14] == 'B':
    dfs = extract_dataframes(EXERCISE, offset=6)
elif EXERCISE[14] == 'C':
    dfs = extract_dataframes(EXERCISE, offset=0)
elif EXERCISE[14] == 'O' or 'R' :
    dfs = extract_dataframes(EXERCISE, offset=3)

for i in range(len(dfs)):
    trial = Trial(dfs[i])
    print(i)
    print(trial.count)

    title = str(i) + EXERCISE[14:17] + "anim.mov"
    print(trial.animate(title))
