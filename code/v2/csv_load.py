import tabulate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# The Trial class forms the core of the data extraction from the CSV files. 
# On initialisation, the Python class requires a Pandas DataFrame as input. 
# Each task trial from the CSV files is represented as a dataframe. 
# The most fundamental properties needed are: trial duration, frame count, the kinematics features, and the events. 
# The Trial class uses the attributes of both the Kinematics and Events classes to regroup the information available for a given exercise. 

class Trial:
    """ Trial class used to save and load the complete information, kinematics and events list for a given trial from a dataframe.
        Dataframe are extracted from the raw CSVs, selected kinematics and parameters columns are read. 
        Future kinematics parameters will be added when needed for analysis. 
    """
    def __init__(self, df, name, filter) -> None: 
        self.name = name  # keep track of the exercise #attempt
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
        fig = plt.figure(figsize=(10,6))
        plt.plot(self.kinematics['right_x'],self.kinematics['right_y'],'ro', label='right')
        plt.plot(self.kinematics['left_x'],self.kinematics['left_y'],'bo', label='left')
        plt.plot(self.kinematics['gaze_x'],self.kinematics['gaze_y'],'go', label='gaze')
        plt.xlim([-0.5,0.5]), plt.xlabel("X position (m)")
        plt.ylim([0,1]), plt.ylabel("Y position (m)")
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
    """ Read and list all saccades and fixations registered in the Kinarm trial dataframe. 
        Events are precisely listed as a dictionary, which in turn is called in the Trial superclass.
    """
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
        self.saccades =  [(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze saccade start') | (df_event['Event name'] == 'Gaze saccade end'))][['Event time (s)']].values]
        self.fixations = [(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze fixation start') | (df_event['Event name'] == 'Gaze fixation end'))][['Event time (s)']].values]
        self.blinks =    [(x) for x in df_event.loc[((df_event['Event name'] == 'Gaze blink start') | (df_event['Event name'] == 'Gaze blink end'))][['Event time (s)']].values]


class Kinematics:
    """ Read and store all kinematics attributes, in a dictionary structure to save the values of the selected parameters.
        The kiematics are then called as Trial.kinematics in the Trial superclass.
    """
    def __init__(self, df, filter) -> None:
        self.values = {}
        self.values['gaze_x'] = [float(i) for i in df['Gaze_X']]
        self.values['gaze_y'] = [float(i) for i in df['Gaze_Y']]
        if filter:
            self.values['filtered_x'], self.values['filtered_y'] = medfilt(df, filter)
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
        except: print('',end='')


def extract_dataframes(file, offset=0, encode='utf_8', set=1):
    """ Extracts each individual trials from the raw csv file as individual pd dataframes. 
        Outputs a list of pd dataframes. 
    """
    # Trial line detection
    trials = []
    with open(file, encoding=encode) as infile:
        for cnt, line in enumerate(infile):
            if "Trial #" in line:
                trials.append(cnt)
        trials.append(cnt + 17)
    #process = subprocess.Popen(["wc", "-l", EXERCISE])#, "copy.sh"]) #-> compares the dataframe lenth count with sh and py 
    
    # Since each exercise type has a different formatting norm the name of the files are used to differentiate
    if set == 1: 
        if 'Ball' in file: offset=6
        elif 'Object' in file or 'Visual' in file: offset=3
    if set == 2:
        if 'Ball' in file: offset=6
        elif 'Object' in file or 'Visual' in file: offset=3
    # Dataframes
    dfs = []
    for i, j in enumerate(trials[:-1]):
        dfs.append(pd.read_csv(file,encoding= 'utf8', sep=',', low_memory=False,
                                skiprows = j-offset, nrows=trials[i+1]-trials[i] -17))
    return dfs

def stat(series):
    """ Used to compute the mean(+std) duration of similar events, eg. mean(+std) duration of saccades"""
    ## TODO: for max and min
    lst = []
    if len(series) > 0: # avoids 0 divisions
        for i in range(0, len(series)-1, 2):
            lst.append(series[i+1] - series[i])   # 0: duration in frames, 1: duration in seconds
        arr = np.array(lst)

        return round(np.mean(arr),2), round(np.std(arr),2) 

def medfilt(df, f):
    """ Output the median filtered series from gazeX and Y 
        df: raw dataframe
        f: filter size, in both directions
    """
    # Note: when ran on arrays made only of NaNs, nanmedian outputs NaN
    arrx, arry = [], []
    for i in range(len(df)):
        if not np.isnan(df['Gaze_X'][i]):
            arrx.append(np.nanmedian(df['Gaze_X'][i-f:i+f]))   
            arry.append(np.nanmedian(df['Gaze_Y'][i-f:i+f]))
        else:
            arrx.append(np.nanmedian(df['Gaze_X'][i]))
            arry.append(np.nanmedian(df['Gaze_Y'][i]))
    return arrx, arry

# Annexe
def path_replace(path):
    output  = path.replace('/', '\\')
    return output

def event_table(trial):
    n_sac = np.array(trial.events['saccades']) # contains start and end
    l_sac = n_sac[1::2] - n_sac[::2]           # list of durations
    n_fix = np.array(trial.events['fixations'])
    l_fix = n_fix[1::2] - n_fix[::2] 
    n_blk = np.array(trial.events['blinks'])
    l_blk = n_blk[1::2] - n_blk[::2] 
    tab = pd.DataFrame({'Count': [len(l_sac), len(l_fix), len(l_blk)],
                        'Mean duration (s)': [l_sac.mean(), l_fix.mean(), l_blk.mean()]}, 
                        index=['Saccad', 'Fixats', 'Blinks'])
    print("Events table: \n", tabulate.tabulate(tab, headers='keys', tablefmt='psql', showindex=True), sep="")

if __name__ == '__main__':
    print("This file should not be run individually.")