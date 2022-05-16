import os
from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation
from alive_progress import alive_bar

# Important note: when saving with mp4 , the save_count parameter is of main importance. 
# It can be lowered to have shorter final animation time. It is dependent of the saving speed: faster plots -> less points -> less save_count.  

def save_cb(current:int, total:int):    
    """ Callback function to track progress during the saving process. """
    if current%100 == 0: print(f'Saving frame {current} of {total}')

# def save_cb2(current:int, total:int): 
#     WIP -> callback.py   
#     """ Callback function to track progress during the saving process. """
#     if current%100 == 0: 
#         print(f'Saving frame {current} of {total}')
#         with alive_bar(total) as bar:
#         for current in range(total):
#             print(bar.current())

def animate_gaze_single(trial, speed:int=1, plot=True, save=True, filename='animation3_single'):
    """ Function to create a video animation from a trial, only for the gaze data.
        The animation represents the movements of the gaze and the progressive position history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
    except: print("no balls",end="")
    
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        return line, 

    def anim(i):
        i = i*speed
        try: ax2.title.set_text(trial.kinematics['frame'][i])
        except: print("",end="")
        line[0].set_data(x[:i],y[:i])
        try: line[1].set_data(bx[:i],by[:i])
        except: 'bx/by do not exist'
        return line

    fig = plt.figure(figsize=(5,6))
    fig.suptitle(("Trial " + str(trial.name) + " Gaze only"))
    ax2 = fig.add_subplot(111)
    line2, = ax2.plot([], [], lw=2)
    line3, = ax2.plot([], [], lw=3, color='r')
    line = [line2, line3]
    for ax in [ax2]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = './animations/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def animate_gaze_triple(trial, speed:int=1, plot=True, save=True, filename='animation3_triple'):
    """ Function a video for a triple frame animation, similar to animate_gaze_single.
        1: gaze position 2: gaze position + history 3: full history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    b=0
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
        b=1
    except: print("no ball data",end="")

    #ax = fig.add_subplot(111)
    #ax.set_ylabel('common ylabel')

    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([x],[y])
        try: 
            line[3].set_data([],[])     #ball line
            line[4].set_data([],[])     #ball line
            line[5].set_data([bx],[by])     #ball line
        except: print("",end="")
        return line, 

    def anim(i):
        i = i*speed
        try : 
            line[0].set_data([x[i], x[i+10]], [y[i], y[i+10]])
            ax1.title.set_text(("Time(s): " + str(round(trial.kinematics['frame_s'][i],4))))
            ax2.title.set_text(("Frame : " + str(trial.kinematics['frame'][i])))
        except: print("",end="")
        line[1].set_data(x[:i],y[:i])
        try:    
            line[3].set_data([bx[i], bx[i+10]], [by[i], by[i+10]])
            line[4].set_data(bx[:i],by[:i])
        except: print("",end="")
        return line

    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(15,6))
    fig.suptitle(("Trial " + str(trial.name) + " Gaze only"))#. Speed: " + str(speed)))
    ax3.title.set_text("Total frames: " + str(len(trial.kinematics['frame'])))
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)'), ax3.set_xlabel('Gaze X position (m)')
    line1, = ax1.plot([], [], lw=2)
    line2, = ax2.plot([], [], lw=2)
    line3, = ax3.plot([], [], lw=2, label = 'gaze')
    line4, = ax1.plot([], [], lw=2)
    line5, = ax2.plot([], [], lw=2)
    if b == 1: line6, = ax3.plot([], [], lw=2, label = 'ball')
    else: line6, = ax3.plot([], [], lw=2,)
    line = [line1, line2, line3, line4, line5, line6]
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(-0.4,0.4)
        ax.set_ylim(0,1)

    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = './animations/final/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
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
            ax1.title.set_text(("Time(s): " + str(round(trial.kinematics['frame_s'][i],4))))
            ax2.title.set_text(("Frame : " + str(trial.kinematics['frame'][i])))
        except:print("",end="")
        #if i%100==0: #ax1.plot(x[:i], y[:i], color='b')
        line[3].set_data(x[:i],y[:i])
        line[4].set_data(x1[:i],y1[:i])
        line[5].set_data(x2[:i],y2[:i])
        return line

    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,6))
    fig.suptitle(("Trial " + str(trial.name)))# + " speed: " + str(speed)))
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
        title = './animations/animation3_all_s' + str(speed) + '.mp4'
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