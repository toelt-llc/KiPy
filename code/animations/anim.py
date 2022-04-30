from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation
from time import sleep

# Important note: when saving with mp4 , the save_count parameter if of main importance. 
# It can be lowered to have shorter final animation time.

def save_cb(current:int, total:int):    
    """ Callback function to track progress during the saving process. """
    if current%100 == 0: print(f'Saving frame {current} of {total}')

def animate_gaze_single(trial, save=True, plot=True):
    """ Function to create a video animation from a trial, only for the gaze data.
        The animation represents the movements of the gaze and the progressive position history.
    """
    def init():
        line[0].set_data([],[])
        return line, 

    def anim(i):
        x = trial.kinematics['gaze_x']
        y = trial.kinematics['gaze_y']
        try: ax2.title.set_text(trial.kinematics['frame'][2*i])
        except: print("",end="")
        line[0].set_data(x[:2*i],y[:2*i])
        return line

    fig = plt.figure(figsize=(5,6))
    fig.suptitle(("Trial " + str(trial.name) + " Gaze only"))
    ax2 = fig.add_subplot(111)
    line2, = ax2.plot([], [], lw=2)
    line = [line2]
    for ax in [ax2]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/2)
    if save: ani.save('./animations/animation3_single.mp4', fps=100, progress_callback=save_cb)
    if plot: plt.show()

def animate_gaze_triple(trial, save=True, plot=True):
    """ Function a video for a triple frame animation, similar to animate_gaze_single.
        1: gaze position 2: gaze position + history 3: full history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']

    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([x],[y])
        return line, 

    def anim(i):
        try : 
            line[0].set_data([x[2*i], x[2*i+10]], [y[2*i], y[2*i+10]])
            ax2.title.set_text(trial.kinematics['frame'][2*i])
        except: print("",end="")
        line[1].set_data(x[:2*i],y[:2*i])
        return line

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

    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/2)
    if save: ani.save('./animations/animation3_triple.mp4', fps=100, progress_callback=save_cb)
    if plot: plt.show()

def animate_all(trial, save=True, plot=True, speed:int=1):
    """ Function plotting a triple animation, similar to the gaze triple.
        Includes right and left hand data. 1: positions 2: positions + history 3: full history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    x1 = trial.kinematics['right_x']
    y1 = trial.kinematics['right_y']
    x2 = trial.kinematics['left_x']
    y2 = trial.kinematics['left_y']

    def init():
        for l in line:
            l.set_data([],[])
        line7.set_data(x,y)
        line8.set_data(x1,y1)
        line9.set_data(x2,y2)
        return line

    def anim(i):
        i = i*speed
        try:
            line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
            line[1].set_data([x1[i], x1[i+10]], [y1[i], y1[i+10]])
            line[2].set_data([x2[i], x2[i+10]], [y2[i], y2[i+10]])
            ax1.title.set_text(("Time : " + str(trial.kinematics['frame_s'][i])))
            ax2.title.set_text(("Frame : " + str(trial.kinematics['frame'][i])))
        except:print("",end="")
        #if i%100==0: #ax1.plot(x[:i], y[:i], color='b')
        line[3].set_data(x[:i],y[:i])
        line[4].set_data(x1[:i],y1[:i])
        line[5].set_data(x2[:i],y2[:i])
        return line

    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,6))
    fig.suptitle(("Trial " + str(trial.name) + " speed: " + str(speed)))
    ax3.title.set_text(len(trial.kinematics['frame']))
    line1, = ax1.plot([], [], lw=5, color='g')
    line2, = ax1.plot([], [], lw=3, color='r')
    line3, = ax1.plot([], [], lw=3, color='b')
    line4, = ax2.plot([], [], lw=5, color='g', label='gaze')
    line5, = ax2.plot([], [], lw=3, color='r', label='right')
    line6, = ax2.plot([], [], lw=3, color='b', label='left')
    line7, = ax3.plot([], [], lw=5, color='g', label='gaze')
    line8, = ax3.plot([], [], lw=3, color='r', label='right')
    line9, = ax3.plot([], [], lw=3, color='b', label='left')
    line = [line1, line2, line3, line4, line5, line6]
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)
    plt.legend()
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        title = './animations/animation2_s' + str(speed) + '.mp4'
        ani.save(title, progress_callback = save_cb, fps=100)
        print('Animation saved under :', title)
    if plot: plt.show()

def armspeed(trial):
    """ Function to plot the arms speed over time for a given trial
    """
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['right_spd'], label='right arm')
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['left_spd'], label='left arm')
    plt.title('Arms speed')
    plt.legend()
    plt.show()

def img_list(trial):
    ## TODO function to do animations from a saved set of frames - unused at the moment 
    fig, (ax1) = plt.subplots(1,1,figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.name)))

    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    for i in range(trial.count):
        ax1.plot(x[i], y[i])
        plt.savefig()