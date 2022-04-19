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

        self.events = []
        self.events_cnt = 0

        self.kinematics = Kinematics(df).values
        #self.plot = self.plots()

    def plots(self,name="fig_default.png"):
        fig = plt.figure()
        floatx = [float(i) for i in self.kinematics['right_x']]
        floaty = [float(i) for i in self.kinematics['right_y']]
        plt.plot(floatx, floaty,'ro', label='right')
        #plt.plot(dataframe['Left: Hand position X'],dataframe['Left: Hand position Y'],'bo', label='left')
        #plt.plot(dataframe['Gaze_X'],dataframe['Gaze_Y'],'go', label='gaze')

        plt.legend()

        plt.savefig(name)
        #plt.show()
        #plt.close(fig)
        return fig 

class Event:
    def __init__(self) -> None:
        self.frame = 0
        self.frame_time = 0
        self.event_name = ""

class Kinematics:
    def __init__(self, df) -> None:
        self.values = {}
        self.values['gaze_x'] = list(df['Gaze_X'])
        self.values['gaze_y'] = list(df['Gaze_Y'])
        self.values['right_x'] = list(df['Right: Hand position X'])
        self.values['right_y'] = list(df['Right: Hand position Y'])
        self.values['right_spd'] = list(df['Right: Hand speed'])
        self.values['left_x'] = list(df['Left: Hand position X'])
        self.values['left_y'] = list(df['Left: Hand position X'])
        self.values['left_spd'] = list(df['Left: Hand speed'])
