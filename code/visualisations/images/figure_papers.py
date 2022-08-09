#!/usr/bin/env python3
import sys
sys.path.append('../../')
import time, pickle, blosc, os
from csv_load import *


start_time = time.time()

DIR = "../../../files/pickles/2/"
FILES = []
for root, dir, files in os.walk(DIR, topdown=False):
    for file in sorted(files):
        FILES.append(os.path.join(root, file))
print(FILES)

for pickled_dfs in FILES[:-2]:
    if pickled_dfs[19] == 'B':
        with open(pickled_dfs, "rb") as f:
            compressed_pickle = f.read()
        depressed_pickle = blosc.decompress(compressed_pickle)
        dfs = pickle.loads(depressed_pickle)
        print("The input file {} contains {} trials.".format(pickled_dfs ,len(dfs)))

        for i in range(len(dfs)):
            trial = Trial(dfs[i], 'default name', filter=None)
            x = trial.kinematics['gaze_x']
            y = trial.kinematics['gaze_y']
            t = trial.kinematics['frame_s']
            b = False
            try:
                bx, by = trial.kinematics['ball_x'], trial.kinematics['ball_y']
                b = True
            except: print("",end="")

            fig, (ax1,ax2) = plt.subplots(2,1, sharex=True, figsize= (13,9))
            ax1.plot(t,y), ax1.set_ylabel('Gaze X position (m)')
            ax2.plot(t,x), ax2.set_ylabel('Gaze Y position (m)')
            if b: 
                ax1.plot(t,by, color='lightgreen')
                ax2.plot(t,bx, color='lightgreen')
            ax2.set_xlabel('Trial time (s)')
            plt.tight_layout()
            fig.align_ylabels()
            #plt.savefig('./paper/gaze_XY2.eps', format='eps')
            plt.show()

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))