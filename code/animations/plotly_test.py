import plotly.graph_objects as go
from csv_load import *
import numpy as np


practice_object = "../../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"

EXERCISE = practice_object

if EXERCISE[17] == 'B':
    dfs = extract_dataframes(EXERCISE, offset=6)
elif EXERCISE[17] == 'C':
    dfs = extract_dataframes(EXERCISE, offset=0)
elif EXERCISE[17] == 'O' or 'R' :
    dfs = extract_dataframes(EXERCISE, offset=3)

trial = Trial(dfs[0])
x = trial.kinematics['gaze_x']#[:1000]
y = trial.kinematics['gaze_y']#[:1000]
t = trial.kinematics['frame_s']

#Number of stops
N = int(trial.duration)

xm = -1
xM = 1
ym = 0
yM = 1

# Create figure
fig = go.Figure(
    data=[go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue"))],
    layout=go.Layout(
        xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
        yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
        title_text=practice_object, hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play", method="animate",
                                        args=[None, {"frame": {"duration": 50, 
                                                                "redraw": False},
                                                                "fromcurrent": True, 
                                                                "transition": {"duration":0 }}])])]),
    frames=[go.Frame(
        data=[go.Scatter(
            x=[x[k]],
            y=[y[k]],
            mode="markers+text",
            marker=dict(color="red", size=20),
            name=t[k],
            text=t[k],
            ids=t)])
            
        for k in range(0,int(trial.count),N)]
)

fig.show()