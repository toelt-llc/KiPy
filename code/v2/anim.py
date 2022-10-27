import os
from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.ndimage import median_filter
#from alive_progress import alive_bar

# Module containing the animations methods

# Important note: when saving with mp4 , the save_count parameter is of main importance. 
# It can be lowered to have shorter final animation time. It is dependent of the saving speed: faster plots -> less points -> less save_count.  

def save_cb(current:int, total:int):    
    """ Callback function to track progress during the saving process. """
    if current%100 == 0: print(f'Saving frame {current} of {total}')

def animate_gaze_double(trial, speed:int=1, plot=True, save=True, filename='animation_double'):
    """ Function to create a video for a double frame animation, similar to animate_gaze_single.
        1: gaze position 2: gaze position + history. Support for ball on bar too. 
    """
    x = trial.kinematics['gaze_x']      # l0,l1
    y = trial.kinematics['gaze_y']      # l0,l1
    rx = trial.kinematics['right_x']    # l4,l5
    ry = trial.kinematics['right_y']    # l4,l5
    lx = trial.kinematics['left_x']     # l6,l7
    ly = trial.kinematics['left_y']     # l6,l7
    b=0
    try: 
        bx = trial.kinematics['ball_x'] # l2,l3
        by = trial.kinematics['ball_y'] # l2,l3
        b=1
    except: None#print("no ball data",end="")

    def anim(i):
        i = i*speed
        try : 
            line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
            line[4].set_data([rx[i], rx[i+10]], [ry[i], ry[i+10]])
            line[6].set_data([lx[i], lx[i+10]], [ly[i], ly[i+10]])
            ax1.title.set_text(("Time (s): " + str(round(trial.kinematics['frame_s'][i],4))))
            ax2.title.set_text(("Frame : " + str(trial.kinematics['frame'][i])))
        except: print("",end="")
        line[2].set_data(x[:i][::10],y[:i][::10])
        line[5].set_data(rx[:i][::10],ry[:i][::10])
        line[7].set_data(lx[:i][::10],ly[:i][::10])
        try:    
            line[1].set_data([bx[i], bx[i+10]], [by[i], by[i+10]])
            line[3].set_data(bx[:i][::10],by[:i][::10])
            #if not np.isnan(x[i]):
            #    ax1.text(0.5, 0.5, f"Gaze-ball distance={np.linalg.norm(np.array([x[i], y[i]]) - np.array([bx[i], by[i]]))}")
        except: print("",end="")
        return line

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,8))
    fig.suptitle((f"Gaze only, speed:  x{str(speed)} \n {trial.name}"))
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    line0, = ax1.plot([], [], "+", lw=5, label = 'gaze')
    line1, = ax1.plot([], [])
    line2, = ax2.plot([], [], lw=2, label = 'gaze', color='lightblue')
    line3, = ax2.plot([], [])
    line4, = ax1.plot([], [], color='green', label = 'right')
    line5, = ax2.plot([], [], color='green', label = 'right')
    line6, = ax1.plot([], [], color='red', label = 'left')
    line7, = ax2.plot([], [], color='red', label = 'left')

    if b == 1: 
        line1, = ax1.plot([], [], "o", lw=5, label = 'ball')
        line3, = ax2.plot([], [], lw=2, label = 'ball')
    line = [line0, line1, line2, line3, line4, line5, line6, line7]
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)

    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = filename + '.mp4'
        if not os.path.isfile(path): 
            print(f"Saving anim to {path}")
            ani.save(path, fps=100, progress_callback=save_cb)
        else: print(f"File already exists: {path}")
    if plot: plt.show()

def animate_all(trial, speed:int=1, save=True, plot=True, filename='animation_all'):
    """ Function plotting a triple animation, similar to the gaze triple but includes hands positions.
        Includes right and left hand data. 1: positions 2: positions + history 3: full position history.
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
            ax1.title.set_text(("Time (s): " + str(round(trial.kinematics['frame_s'][i],4))))
            ax2.title.set_text(("Frame : " + str(trial.kinematics['frame'][i])))
        except:print("",end="")
        #if i%100==0: #ax1.plot(x[:i], y[:i], color='b')
        line[3].set_data(x[:i],y[:i])
        line[4].set_data(x1[:i],y1[:i])
        line[5].set_data(x2[:i],y2[:i])
        return line

    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,6))
    fig.suptitle(("Trial " + str(trial.name) + " gaze & hands"))# + " speed: " + str(speed)))
    ax3.title.set_text("Total frames: " + str(len(trial.kinematics['frame'])))
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)'), ax3.set_xlabel('Gaze X position (m)')
    line1, = ax1.plot([], [], lw=5, color='g')
    line2, = ax1.plot([], [], lw=3, color='r')
    line3, = ax1.plot([], [], lw=3, color='b')
    line4, = ax2.plot([], [], lw=5, color='g', label='gaze')
    line5, = ax2.plot([], [], lw=3, color='r', label='right hand')
    line6, = ax2.plot([], [], lw=3, color='b', label='left')
    line7, = ax3.plot([], [], lw=5, color='g', label='gaze')
    line8, = ax3.plot([], [], lw=3, color='r', label='right hand')
    line9, = ax3.plot([], [], lw=3, color='b', label='left hand')
    line = [line1, line2, line3, line4, line5, line6]
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        title = './animations/' + filename + '.mp4'
        ani.save(title, progress_callback = save_cb, fps=100)
        print('Animation saved under :', title)
    if plot: plt.show()

def armspeed(trial, plot=True, save=True, filename='arms_speed'):
    """ Function to plot the arms speed over time for a given trial
    """
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['right_spd'], label='right arm')
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['left_spd'], label='left arm')
    plt.suptitle('Arms speed')
    plt.title(trial.name, fontsize=10)
    plt.xlabel("Time (s)")
    plt.ylabel("Hand speed (m/s)")
    plt.legend()
    if save: 
        path = filename + '.svg'
        plt.savefig(path)
    if plot: plt.show()

def plot_eyes(trial, plot = True, save = True, filename = 'figure5'):
    pass
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']

