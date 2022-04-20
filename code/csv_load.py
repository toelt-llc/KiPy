import pandas as pd
import matplotlib.pyplot as plt

def extract_dataframes(file, offset=0, encode='utf_8'):
    """ TODO
    """
    # Line detection
    trials = []
    with open(file, encoding=encode) as infile:
        for cnt, line in enumerate(infile):
            if "Trial #" in line:
                trials.append(cnt)
        trials.append(cnt + 17)
        #process = subprocess.Popen(["wc", "-l", EXERCISE])#, "copy.sh"])
    # Dataframes
    dfs = []
    for i, j in enumerate(trials[:-1]):
        dfs.append(pd.read_csv(file,encoding= 'utf8', sep=',', low_memory=False,
                                skiprows = j-offset, nrows=trials[i+1]-trials[i] -17))

    return dfs

class Trial:
    def __init__(self, df) -> None:
        self.name = df.iloc[0][0]
        self.rate = df.iloc[0][3]
        self.count = df.iloc[0][4]
        self.duration = df.iloc[-1][10]

        self.events_cnt = Events(df).counts
        self.saccades = Events(df).saccades
        self.fixations = Events(df).fixations
        self.blinks = Events(df).blinks
        self.events = {'saccades':self.saccades, 'fixations':self.fixations, 'blinks':self.blinks}

        self.kinematics = Kinematics(df).values
        #self.plot = self.plots()

    def plot_movements(self,name="fig_default.png", save=True, show=False):
        fig = plt.figure()
        plt.plot(self.kinematics['right_x'],self.kinematics['right_y'],'ro', label='right')
        plt.plot(self.kinematics['left_x'],self.kinematics['left_y'],'bo', label='left')
        plt.plot(self.kinematics['gaze_x'],self.kinematics['gaze_y'],'go', label='gaze')
        plt.legend()
        plt.title(self.duration)

        if save: plt.savefig(name)
        if show: plt.show()
        else: plt.close(fig)
        return fig 

class Events:
    def __init__(self, df) -> None:
        event_list = list(df[df['Event name'].notna()]['Event name'])
        self.counts = {}
        self.counts['saccades'] = event_list.count('Gaze saccade start')
        self.counts['fixations'] = event_list.count('Gaze fixation start')
        self.counts['blinks'] = event_list.count('Gaze blink start')
        #self.counts['other'] = event_list.count('')
        df_event = df[df['Event name'].notna()]
        self.saccades =  [tuple(x) for x in df_event.loc[df_event['Event name'] == 'Gaze saccade start'][['Frame #','Event time (s)']].values]
        self.fixations = [tuple(x) for x in df_event.loc[df_event['Event name'] == 'Gaze fixation start'][['Frame #','Event time (s)']].values]
        self.blinks =    [tuple(x) for x in df_event.loc[df_event['Event name'] == 'Gaze blink start'][['Frame #','Event time (s)']].values]

        
class Kinematics:
    def __init__(self, df) -> None:
        self.values = {}
        self.values['gaze_x'] = [float(i) for i in df['Gaze_X']]
        self.values['gaze_y'] = [float(i) for i in df['Gaze_Y']]
        self.values['right_x'] = list(df['Right: Hand position X'])
        self.values['right_y'] = list(df['Right: Hand position Y'])
        self.values['right_spd'] = list(df['Right: Hand speed'])
        self.values['left_x'] = list(df['Left: Hand position X'])
        self.values['left_y'] = list(df['Left: Hand position Y'])
        self.values['left_spd'] = list(df['Left: Hand speed'])
