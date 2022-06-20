import os

from sqlalchemy import false
from csv_load import *
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.ndimage import median_filter
from alive_progress import alive_bar

# Module containing the animations methods

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

def animate_gaze_single(trial, speed:int=1, plot=True, save=True, filename='animation_single'):
    """ Function to create a video animation from a trial, only for the gaze data.
        The animation represents the movements of the gaze and the progressive position history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
    except: print("",end="")
    
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        return line, 

    def anim(i):
        i = i*speed
        try: ax2.title.set_text(trial.kinematics['frame_s'][i])
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
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = './animations/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def animate_gaze_triple(trial, speed:int=1, plot=True, save=True, filename='animation_triple'):
    """ Function to create a video for a triple frame animation, similar to animate_gaze_single.
        1: gaze position 2: gaze position + history 3: full position history.
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
            ax1.title.set_text(("Time (s): " + str(round(trial.kinematics['frame_s'][i],4))))
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
        path = './animations/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
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

def animate_gaze_single_medfilt_old(trial, speed:int=1, filter=3, plot=True, save=True, filename='outdated'):
    """ Function to create a video animation from a trial, only for the gaze data.
        The animation represents the movements of the gaze and the progressive position history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    x_med = median_filter(trial.kinematics['gaze_x'],filter)
    y_med = median_filter(trial.kinematics['gaze_y'],filter)
    b = 0
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
        b = 1
    except: print("",end="")
    
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([],[])
        line[3].set_data([],[])
        return line, 

    def anim(i):
        i = i*speed
        try: time_text.set_text(trial.kinematics['frame_s'][i])
        except: print("",end="")
        line[0].set_data(x[:i],y[:i])
        line[2].set_data(x_med[:i],y_med[:i])
        try: 
            line[1].set_data(bx[:i],by[:i])
            line[3].set_data(bx[:i],by[:i])
        except: 'bx/by do not exist'
        return line, 

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.num) + trial.name))
    time_text = ax1.text(0.95, 0.95,'', ha='right', va='top',transform=ax1.transAxes)
    ax1.text(0.96, 0.98,'Time (s)', ha='right', va='top',transform=ax1.transAxes)
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    ax1.title.set_text("Original"), ax2.title.set_text("Filtered: " + str(filter) + " (ms) median")
    line1, = ax1.plot([], [], lw=2)
    line3, = ax2.plot([], [], lw=2, label='gaze')
    if b == 1: 
        line2, = ax1.plot([], [], lw=3, color='r')
        line4, = ax2.plot([], [], lw=3, color='r', label = 'ball')
    else: 
        line2, = ax1.plot([], [])
        line4, = ax2.plot([], [])
    line = [line1, line2, line3, line4]
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = './animations/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def animate_gaze_single_medfilt(trial, speed:int=1, plot=True, save=True, filename='animation_singlefilt'):
    """ Function to create a video animation from a trial, only for the gaze data.
        The animation represents the movements of the gaze and the progressive position history.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    # x_med = median_filter(trial.kinematics['gaze_x'],filter)
    # y_med = median_filter(trial.kinematics['gaze_y'],filter)
    x_med = trial.kinematics['filtered_x']
    y_med = trial.kinematics['filtered_y']
    b = 0
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
        b = 1
    except: print("",end="")
    
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([],[])
        line[3].set_data([],[])
        return line, 

    def anim(i):
        i = i*speed
        try: time_text.set_text(trial.kinematics['frame_s'][i])
        except: print("",end="")
        line[0].set_data(x[:i],y[:i])
        line[2].set_data(x_med[:i],y_med[:i])
        try: 
            line[1].set_data(bx[:i],by[:i])
            line[3].set_data(bx[:i],by[:i])
        except: 'bx/by do not exist'
        return line, 

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.num) + trial.name))
    time_text = ax1.text(0.95, 0.95,'', ha='right', va='top',transform=ax1.transAxes)
    ax1.text(0.96, 0.98,'Time (s)', ha='right', va='top',transform=ax1.transAxes)
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    ax1.title.set_text("Original"), ax2.title.set_text("Filtered: " + str(trial.filter_size*2) + " (ms) median")
    line1, = ax1.plot([], [], lw=2)
    line3, = ax2.plot([], [], lw=2, label='gaze')
    if b == 1: 
        line2, = ax1.plot([], [], lw=3, color='r')
        line4, = ax2.plot([], [], lw=3, color='r', label = 'ball')
    else: 
        line2, = ax1.plot([], [])
        line4, = ax2.plot([], [])
    line = [line1, line2, line3, line4]
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=trial.count/speed)
    if save:
        path = './animations/newfilter/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def static_gaze_single_medfilt(trial, plot=True, save=True, filename='static_singlefilt'):
    """ Function to create a static image from a trial and apply the median filter, only for the gaze data.
    """
    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    x_med = trial.kinematics['filtered_x']
    y_med = trial.kinematics['filtered_y']
    b = 0
    try: 
        bx = trial.kinematics['ball_x']
        by = trial.kinematics['ball_y']
        b = 1
    except: print("",end="")
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.num) + trial.name))
    ax1.text(0.95, 0.95, round(trial.duration,2) , ha='right', va='top',transform=ax1.transAxes)
    ax1.text(0.96, 0.98,'Time (s)', ha='right', va='top',transform=ax1.transAxes)
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    ax1.title.set_text("Original"), ax2.title.set_text("Filtered: " + str(trial.filter_size*2) + " (ms) median")
    line1, = ax1.plot([], [], lw=2)
    line2, = ax1.plot([], [], lw=3, color='r')
    line3, = ax2.plot([], [], lw=2, label='gaze')
    line4, = ax2.plot([], [], lw=3, color='r', label = 'ball')
    if b == 1:
        line2.set_data(bx,by)
        line4.set_data(bx,by)
    line1.set_data(x,y)
    line3.set_data(x_med,y_med)
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()

    if save:
        path = './animations/newfilter/' + filename + '.png'
        if not os.path.isfile(path): plt.savefig(path, fps=100)#, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def armspeed(trial, plot=True, save=True, filename='arms_speed.svg'):
    """ Function to plot the arms speed over time for a given trial
    """
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['right_spd'], label='right arm')
    plt.plot(trial.kinematics['frame_s'], trial.kinematics['left_spd'], label='left arm')
    plt.title('Arms speed trial {}'.format(trial.name))
    plt.xlabel("Time (s)")
    plt.ylabel("Hand speed (m/s)")
    plt.legend()
    if save: 
        path = './images/' + filename + '.svg'
        plt.savefig(path)
    if plot: plt.show()

def img_list(trial):
    ## TODO function to do animations from a saved set of frames - unused at the moment 
    fig, (ax1) = plt.subplots(1,1,figsize=(10,6))
    fig.suptitle(("Trial " + str(trial.name)))

    x = trial.kinematics['gaze_x']
    y = trial.kinematics['gaze_y']
    for i in range(trial.count):
        ax1.plot(x[i], y[i])
        plt.savefig()

# DF only - used in notebooks
def animate_simple_medfilt(dforigin, dffilter, filter = 7, speed:int=1, plot=True, save=True, filename='animation_filter'):
    """ Function to create a video animation from a dataframe, only for the gaze data.
        Used for the 2nd dataframe to compare normal and filtered data.
    """
    x = dforigin['Gaze_X']
    y = dforigin['Gaze_Y']
    x_med = dffilter['X filter']
    y_med = dffilter['Y filter']
    # b = 0 
    # try: 
    #     bx = trial.kinematics['ball_x']
    #     by = trial.kinematics['ball_y']
    #     b = 1
    # except: print("",end="")
    
    def init():
        line[0].set_data([],[])
        line[1].set_data([],[])
        line[2].set_data([],[])
        line[3].set_data([],[])
        return line, 

    def anim(i):
        i = i*speed
        try: time_text.set_text(dffilter['Frame time (s)'][i])
        except: print("",end="")
        line[0].set_data(x[:i],y[:i])
        line[2].set_data(x_med[:i],y_med[:i])
        # try: 
        #     line[1].set_data(bx[:i],by[:i])
        #     line[3].set_data(bx[:i],by[:i])
        # except: 'bx/by do not exist'
        return line, 

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6))
    fig.suptitle(("Filtered comparison "))# + str(trial.num) + trial.name))
    time_text = ax1.text(0.95, 0.95,'', ha='right', va='top',transform=ax1.transAxes)
    ax1.text(0.96, 0.98,'Time (s)', ha='right', va='top',transform=ax1.transAxes)
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    ax1.title.set_text("Original"), ax2.title.set_text("Filtered: " + str(filter) + " (ms) median")
    line1, = ax1.plot([], [], lw=2)
    line3, = ax2.plot([], [], lw=2, label='gaze')
    # if b == 1: 
    #     line2, = ax1.plot([], [], lw=3, color='r')
    #     line4, = ax2.plot([], [], lw=3, color='r', label = 'ball')
    # else: 
    line2, = ax1.plot([], [])
    line4, = ax2.plot([], [])
    line = [line1, line2, line3, line4]
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, anim, init_func=init, interval=1, blit=False, repeat=False, save_count=len(dffilter)/speed)
    if save:
        path = './animations/' + filename + '.mp4'
        if not os.path.isfile(path): ani.save(path, fps=100, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()

def static_simple_medfilt(dforigin, dffilter, filter=7, plot=True, save=True, filename='static_filter'):
    """ Function to create a static image from a dataframe, only for the gaze data.
        Used for the 2nd dataframe to compare normal and filtered data.
    """
    x = dforigin['Gaze_X']
    y = dforigin['Gaze_Y']
    x2 = dffilter['X filter']
    y2 = dffilter['Y filter']
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,6))
    fig.suptitle(("Plot from dataframe "))# + str(trial.num) + trial.name))
    ax1.text(0.95, 0.95, round(dffilter.iloc[-1]['Frame time (s)'],2) , ha='right', va='top',transform=ax1.transAxes)
    ax1.text(0.96, 0.98,'Total time (s)', ha='right', va='top',transform=ax1.transAxes)
    ax1.set_ylabel('Gaze Y position (m)')
    ax1.set_xlabel('Gaze X position (m)'), ax2.set_xlabel('Gaze X position (m)')
    ax1.title.set_text("Original"), ax2.title.set_text("Filtered: " + str(filter) + " (ms) median")

    line1, = ax1.plot([], [], lw=2)
    line3, = ax2.plot([], [], lw=2, label='gaze')
    
    line1.set_data(x,y)
    line3.set_data(x2,y2)
    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.1,1)
    plt.legend(title = 'Positions')
    plt.tight_layout()

    if save:
        path = './images/' + filename + '.png'
        if not os.path.isfile(path): plt.savefig(path, fps=100)#, progress_callback=save_cb)
        else: print("File already exists.")
    if plot: plt.show()