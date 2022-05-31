import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Trial module automatically loads the CSVs as dataframes and export the desired columns.
# Future parameters will be added when needed for analysis.  

class Trial:
    """ doc
    """
    def __init__(self, df, name, filter) -> None: 
        self.name = name  # variable to keep track of the exercise 
        self.num = df.iloc[0][0]
        self.rate = df.iloc[0][3]
        self.count = df.iloc[0][4]
        self.duration = round(df.iloc[-1][10],4)
        self.filter_size = filter

        self.events_cnt = Events(df).counts
        self.saccades = Events(df).saccades
        self.fixations = Events(df).fixations
        self.blinks = Events(df).blinks
        self.events = {'saccades':self.saccades, 'fixations':self.fixations, 'blinks':self.blinks}
        self.event_mean = {'saccades':stat(self.events['saccades']), 'fixations':stat(self.events['fixations']), 
                             'blinks':stat(self.events['blinks'])}
        self.event_list = Events(df).event_list

        self.kinematics = Kinematics(df, filter).values
        #self.plot = self.plots()

    def plot_movements(self,name="fig_default.png", save=False, show=True):
        fig = plt.figure()
        plt.plot(self.kinematics['right_x'],self.kinematics['right_y'],'ro', label='right')
        plt.plot(self.kinematics['left_x'],self.kinematics['left_y'],'bo', label='left')
        plt.plot(self.kinematics['gaze_x'],self.kinematics['gaze_y'],'go', label='gaze')
        plt.xlim([-0.5,0.5])
        plt.ylim([0,1])
        plt.legend()
        plt.title("Summary plot. Duration : " + str(self.duration))

        if save: plt.savefig(name)
        if show: plt.show()
        else: plt.close(fig)
        return fig 

    def animate(self, name="anim_default.gif", save=True, show=False):
        fig, ax = plt.subplots()
        def animate(i):
            ax.plot(self.kinematics['right_x'][i],self.kinematics['right_y'][i],'ro', label='right')
            ax.plot(self.kinematics['left_x'][i],self.kinematics['left_y'][i],'bo', label='left')
            ax.plot(self.kinematics['gaze_x'][i],self.kinematics['gaze_y'][i],'go', label='gaze')
            ax.set_xlim([-0.5,0.5])
            ax.set_ylim([0,1])

        plt.legend()
        anim = FuncAnimation(fig, animate, interval=5, repeat=False, save_count=1500) #frames=int(len(gazeX)/4)
        
        if save: anim.save(name, fps=30)
        if show: plt.show()
        else: plt.close()


class Events:
    def __init__(self, df) -> None:
        event_list = list(df[df['Event name'].notna()]['Event name'])
        self.event_list = event_list
        self.counts = {}
        self.counts['saccades'] = event_list.count('Gaze saccade start')
        self.counts['fixations'] = event_list.count('Gaze fixation start')
        self.counts['blinks'] = event_list.count('Gaze blink start')
        #self.counts['other'] = event_list.count('')
        df_event = df[df['Event name'].notna()]
        # Returns tuple with the Frame# and time at which start OR end happens, order is always start->end
        self.saccades =  [tuple(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze saccade start') | (df_event['Event name'] == 'Gaze saccade end'))][['Frame #','Event time (s)']].values]
        self.fixations = [tuple(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze fixation start') | (df_event['Event name'] == 'Gaze fixation end'))][['Frame #','Event time (s)']].values]
        self.blinks =    [tuple(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze blink start') | (df_event['Event name'] == 'Gaze blink end'))][['Frame #','Event time (s)']].values]


class Kinematics:
    def __init__(self, df, filter) -> None:
        self.values = {}
        self.values['gaze_x'] = [float(i) for i in df['Gaze_X']]
        self.values['gaze_y'] = [float(i) for i in df['Gaze_Y']]
        self.values['filtered_x'], _ = medfilt(df, filter)
        _, self.values['filtered_y'] = medfilt(df, filter)
        self.values['right_x'] = list(df['Right: Hand position X'])
        self.values['right_y'] = list(df['Right: Hand position Y'])
        self.values['right_spd'] = list(df['Right: Hand speed'])
        self.values['left_x'] = list(df['Left: Hand position X'])
        self.values['left_y'] = list(df['Left: Hand position Y'])
        self.values['left_spd'] = list(df['Left: Hand speed'])
        self.values['frame'] = list(df['Frame #'])
        self.values['frame_s'] = [round(val,1) for val in list(df['Frame time (s)'])]
        try: 
            self.values['ball_x'] = list(df['x_ball_pos'])
            self.values['ball_y'] = list(df['y_ball_pos'])
        except: print('')


def extract_dataframes(file, offset=0, encode='utf_8', set=1):
    """ Extracts the trials from the raw csv as dataframes. Outputs a list of pd dataframes. 
    """
    # Trial line detection
    trials = []
    with open(file, encoding=encode) as infile:
        for cnt, line in enumerate(infile):
            if "Trial #" in line:
                trials.append(cnt)
        trials.append(cnt + 17)  #process = subprocess.Popen(["wc", "-l", EXERCISE])#, "copy.sh"]) #-> compares the count with sh and py
    
    # Since each exercise type has a different formatting norm the name of the files are used to differentiate
    if set == 1: 
        if file[14] == 'B': offset=6
        elif file[14] == 'O' or file[14] == 'V': offset=3
    if set == 2:
        if file[16] == 'B': offset=6
        elif file[16] == 'O' or file[16] == 'V': offset=3
    # Dataframes
    dfs = []
    for i, j in enumerate(trials[:-1]):
        dfs.append(pd.read_csv(file,encoding= 'utf8', sep=',', low_memory=False,
                                skiprows = j-offset, nrows=trials[i+1]-trials[i] -17))
    return dfs

def stat(series):
    """ Used to compute the mean/std duration of similar events, eg. mean duration of saccades"""
    ## TODO: for max and min
    lst = []
    for i in range(0, len(series)-1, 2):
        lst.append(series[i+1][0] - series[i][0])   # 0: duration in frames, 1: duration in seconds
    arr = np.array(lst)

    return round(np.mean(arr),2), round(np.std(arr),2) 

def medfilt(df, f):
            """ df: raw dataframe
                f: filter size, in both directions
            """
            #newdf = pd.DataFrame()
            arrx, arry = [], []
            for i in range(len(df)):
                arrx.append(np.nanmedian(df['Gaze_X'][i-f:i+f]))
                arry.append(np.nanmedian(df['Gaze_Y'][i-f:i+f]))
            # newdf['X filter'], newdf['Y filter'] = arrx, arry
            # newdf['Frame time (s)'] = df['Frame time (s)']

            return arrx, arry