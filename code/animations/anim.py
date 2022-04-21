from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation

# practice_object = "../../files/utf8/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv"
# ball = "../../files/utf8/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.csv"
# dfs = extract_dataframes(ball, offset=6)#3
# trial = Trial(dfs[2])

def animate(trial, save=True, plot=True):
    """
    """
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([],[])
        return line, 

    def anim(i):
        x = trial.kinematics['gaze_x']
        y = trial.kinematics['gaze_y']
        try: line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
        except:print("",end="")
        if i%100== 0: 
            #ax1.plot(x[:i], y[:i], color='b')
            try:    
                ax1.title.set_text(trial.kinematics['frame'][i])
                ax2.title.set_text(trial.kinematics['frame'][i])
            except: print("",end="")
        line[1].set_data(x[:i],y[:i])
        line[2].set_data(x,y)
        #plt.title(trial.kinematics['frame'][i])
        return line

    # fig = plt.figure()
    # ax = plt.axes(xlim=(-0.5, 1), ylim=(-0.5, 1))
    # line, = ax.plot([], [], lw=5)
    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(15,6))
    fig.suptitle(("Trial " + str(trial.name) + " Gaze only"))
    ax3.title.set_text(len(trial.kinematics['frame']))
    line1, = ax1.plot([], [], lw=2)
    line2, = ax2.plot([], [], lw=2)
    line3, = ax3.plot([], [], lw=2)
    line = [line1, line2, line3]
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)


    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=200)
    #ani.save('animation.gif', fps=200)
    plt.tight_layout()
    plt.show()


def animate2(trial, save=True, plot=True):
    """ TODO
    """
    def init():
        for l in line:
            l.set_data([],[])
        return line, 

    def anim(i):
        x = trial.kinematics['gaze_x']
        y = trial.kinematics['gaze_y']
        x1 = trial.kinematics['right_x']
        y1 = trial.kinematics['right_y']
        x2 = trial.kinematics['left_x']
        y2 = trial.kinematics['left_y']
        try:
            line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
            line[1].set_data([x1[i], x1[i+10]], [y1[i], y1[i+10]])
            line[2].set_data([x2[i], x2[i+10]], [y2[i], y2[i+10]])
        except:print("",end="")
        if i%100== 0: 
            #ax1.plot(x[:i], y[:i], color='b')
            try: 
                ax1.title.set_text(trial.kinematics['frame'][i])
                ax2.title.set_text(trial.kinematics['frame'][i])
            except: print("",end="")
        line[3].set_data(x[:i],y[:i])
        line[4].set_data(x1[:i],y1[:i])
        line[5].set_data(x2[:i],y2[:i])
        # line[2].set_data(x,y)
        return line

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.name)))
    line1, = ax1.plot([], [], lw=3, color='g')
    line2, = ax1.plot([], [], lw=2, color='r')
    line3, = ax1.plot([], [], lw=2, color='b')
    line4, = ax2.plot([], [], lw=3, color='g', label='gaze')
    line5, = ax2.plot([], [], lw=2, color='r', label='right')
    line6, = ax2.plot([], [], lw=2, color='b', label='left')
    line = [line1, line2, line3, line4, line5, line6]
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)

    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=200)
    #ani.save('animation.gif', fps=200)
    plt.legend()
    plt.tight_layout()
    plt.show()

#animate2(trial)
#animate(trial)