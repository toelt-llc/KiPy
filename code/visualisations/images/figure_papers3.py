#!/usr/bin/env python3
import sys
sys.path.append('../../')
import time, pickle, blosc
from csv_load import *

# Filter application on ball on bar

def medfilt(df, f):
    """ df: raw dataframe
        f: filter size, in both directions
    """
    newdf = pd.DataFrame()
    arrx, arry = [], []
    for i in range(len(df)):
        arrx.append(np.nanmedian(df['Gaze_X'][i-f:i+f]))
        arry.append(np.nanmedian(df['Gaze_Y'][i-f:i+f]))
    df['X filter'], df['Y filter'] = arrx, arry
    #newdf['Frame time (s)'] = df['Frame time (s)']

    return df

start_time = time.time()

trial1_ball = '../../../files/pickles/1/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.pickle'
trial2_ball = '../../../files/pickles/2/Ball_on_Bar_-_Child_-_RIGHT_-_10_21.pickle'
trial4_ball = '../../../files/pickles/2/Ball_on_Bar_-_Child_-_RIGHT_-_10_25.pickle'

with open(trial4_ball, "rb") as f:
    compressed_pickle = f.read()
depressed_pickle = blosc.decompress(compressed_pickle)
df = pickle.loads(depressed_pickle)[0]  # only select first element of the list, since only 1 trial in this file
#df = medfilt(df, 7)

#anim.static_simple_medfilt(df, medfilt(df, 7), plot=True, save=False, filename='paperdraft')
trial = Trial(df, 'default name', filter=75)
trialbis = Trial(df, 'default name', filter=250)
trialtri = Trial(df, 'default name', filter=500)

x = trial.kinematics['gaze_x']
y = trial.kinematics['gaze_y']
fx = trial.kinematics['filtered_x']
fy = trial.kinematics['filtered_y']
fx2 = trialbis.kinematics['filtered_x']
fy2 = trialbis.kinematics['filtered_y']
fx3 = trialtri.kinematics['filtered_x']
fy3 = trialtri.kinematics['filtered_y']
t = trial.kinematics['frame_s']
b = False
# try:
#     bx, by = trial.kinematics['ball_x'], trial.kinematics['ball_y']
#     b = True
# except: print("",end="")
style = 'quad'

if style == 'quad': 
    fig, ((ax1, ax2, ax3, ax4),(ax5, ax6, ax7, ax8)) = plt.subplots(2,4, sharex=True, sharey='row', figsize= (17,9))
    #normal
    ax1.plot(t,y, c='k', alpha=0.8), ax1.set_ylabel('GazeY (m)', fontsize=17), ax1.text(0.1,0.85,'Source', fontsize=17)
    ax5.plot(t,x, c='k', alpha=0.8), ax5.set_ylabel('GazeX (m)', fontsize=17), ax5.text(0.1,0.45,'Source', fontsize=17)
    #filter 1
    ax2.plot(t,fy, alpha=0.8), ax2.text(0.1,0.85,'Filter: 150', fontsize=17)
    ax6.plot(t,fx, alpha=0.8), ax6.text(0.1,0.45,'Filter: 150', fontsize=17)
    #filter 2 
    ax3.plot(t,fy2, alpha=0.8), ax3.text(0.1,0.85,'Filter: 500', fontsize=17)
    ax7.plot(t,fx2, alpha=0.8), ax7.text(0.1,0.45,'Filter: 500', fontsize=17)
    #filter 3 
    ax4.plot(t,fy3, alpha=0.8), ax4.text(0.1,0.85,'Filter: 1000', fontsize=17)
    ax8.plot(t,fx3, alpha=0.8), ax8.text(0.1,0.45,'Filter: 1000', fontsize=17)

if style == 'triple': 
    fig, ((ax1, ax2, ax3),(ax4, ax5, ax6)) = plt.subplots(2,3, sharex=True, sharey='row', figsize= (13,9))
    #normal
    ax1.plot(t,y, c='k', alpha=0.8), ax1.set_ylabel('GazeY source (m)', fontsize=17)
    ax4.plot(t,x, c='k', alpha=0.8), ax4.set_ylabel('GazeX source (m)', fontsize=17)
    #filter
    ax2.plot(t,fy, c='k', alpha=0.8), ax2.set_ylabel('GazeY filtered 140 (m)', fontsize=17)
    ax5.plot(t,fx, c='k', alpha=0.8), ax5.set_ylabel('GazeX filtered 140 (m)', fontsize=17)
    #filter 2 
    ax3.plot(t,fy2, c='k', alpha=0.8), ax3.set_ylabel('GazeY filtered2 500 (m)', fontsize=17)
    ax6.plot(t,fx2, c='k', alpha=0.8), ax6.set_ylabel('GazeX filtered2 500 (m)', fontsize=17)

elif style == 'double':
    fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2,2, sharex=True, sharey='row', figsize= (10,7))
    #normal
    ax1.plot(t,y), ax1.set_ylabel('GazeY source (m)')
    ax3.plot(t,x), ax3.set_ylabel('GazeX source (m)')
    #filter
    ax2.plot(t,fy), ax1.text(0.9,0.1,"GazeY filtered")
    ax4.plot(t,fx), ax2.text(0.1,0.8,"GazeX filtered")
# if b: 
#     ax1.plot(t,by, color='lightgreen')
#     ax2.plot(t,bx, color='lightgreen')
ax5.set_xlabel('Trial time (s)', fontsize=17), ax6.set_xlabel('Trial time (s)', fontsize=17)
ax7.set_xlabel('Trial time (s)', fontsize=17), ax8.set_xlabel('Trial time (s)', fontsize=17)
plt.tight_layout()
fig.align_ylabels()
#plt.savefig('./paper/gaze_filter.eps', format='eps')
fig.savefig('./paper/gaze_filter_4.png', format='png', dpi=1200)
plt.show()

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))