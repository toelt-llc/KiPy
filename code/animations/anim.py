from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation

practice_object = "../../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"
ball = "../../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
dfs = extract_dataframes(ball, offset=6)#3
trial = Trial(dfs[2])

#print(len(dfs))
#print(trial.count)
#print(trial.kinematics['gaze_x'])

def init():
    line[0].set_data([],[])
    line[1].set_data([],[])
    return line, 

def animate(i):
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
    if i%100== 0: 
        ax1.plot(x[:i], y[:i], color='b')
        ax1.title.set_text(trial.kinematics['frame'][i])
    line[1].set_data(x,y)
    #plt.title(trial.kinematics['frame'][i])
    return line

# fig = plt.figure()
# ax = plt.axes(xlim=(-0.5, 1), ylim=(-0.5, 1))
# line, = ax.plot([], [], lw=5)

fig, (ax1, ax2) = plt.subplots(2,1)
line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
line = [line1, line2]
for ax in [ax1, ax2]:
    ax.set_ylim(min(trial.kinematics['gaze_y']), 1.2*max(trial.kinematics['gaze_y']))
    ax.set_xlim(min(trial.kinematics['gaze_x']), 1.2*max(trial.kinematics['gaze_x']))


ani = animation.FuncAnimation(fig, animate, init_func=init, interval=1, blit=False, repeat=False, save_count=200)
#ani.save('animation.gif', fps=200)
plt.show()




