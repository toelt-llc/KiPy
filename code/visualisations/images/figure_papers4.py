#!/usr/bin/env python3
import sys
sys.path.append('../../')
import time, pickle, blosc
from csv_load import *

# Same as figure_papers2, but include hands

start_time = time.time()

trial1_ball = '../../../files/pickles/1/Ball_on_Bar_-_Child_-_RIGHT_-_11_59.pickle'
trial2_ball = '../../../files/pickles/2/Ball_on_Bar_-_Child_-_RIGHT_-_10_21.pickle'
trial1_obj = '../../../files/pickles/1/Object_Hit_-_Child_-_RIGHT_-_12_02.pickle'
trial2_obj = '../../../files/pickles/2/Object_Hit_-_Child_-_RIGHT_-_10_28.2.pickle'
trial1_vis = '../../../files/pickles/1/Visually_Guided_Reaching_-_Child_v2_(4_target)_-_LEFT_-_11_50.pickle'
trial2_vis = '../../../files/pickles/2/Visually_Guided_Reaching_-_Child__4_target_-_LEFT_-_10_06.pickle'

with open(trial1_ball, "rb") as f1, open(trial2_ball, 'rb') as f2, open(trial1_obj, "rb") as f3, open(trial2_obj, 'rb') as f4, open(trial1_vis, "rb") as f5, open(trial2_vis, 'rb') as f6:
    compressed_pickle1, compressed_pickle2, compressed_pickle3, compressed_pickle4, compressed_pickle5, compressed_pickle6 = f1.read(), f2.read(), f3.read(), f4.read(), f5.read(), f6.read()
depressed_pickle1, depressed_pickle2, depressed_pickle3, depressed_pickle4, depressed_pickle5, depressed_pickle6 = blosc.decompress(compressed_pickle1), blosc.decompress(compressed_pickle2), blosc.decompress(compressed_pickle3), blosc.decompress(compressed_pickle4), blosc.decompress(compressed_pickle5), blosc.decompress(compressed_pickle6) 
dfs1, dfs2, dfs3, dfs4, dfs5, dfs6 = pickle.loads(depressed_pickle1), pickle.loads(depressed_pickle2), pickle.loads(depressed_pickle3), pickle.loads(depressed_pickle4), pickle.loads(depressed_pickle5), pickle.loads(depressed_pickle6)
#print("The input file {} contains {} trials.".format(pickled_dfs ,len(dfs)))

i = 0
# csv load
trial1b, trial2b = Trial(dfs1[i], 'default name', filter=None), Trial(dfs2[i], 'default name', filter=None)
trial1o, trial2o = Trial(dfs3[i], 'default name', filter=None), Trial(dfs4[i], 'default name', filter=None)
trial1v, trial2v = Trial(dfs5[i], 'default name', filter=None), Trial(dfs6[i], 'default name', filter=None)
# trials
t1b = trial1b.kinematics['frame_s']
t2b = trial2b.kinematics['frame_s']
t1o = trial1o.kinematics['frame_s']
t2o = trial2o.kinematics['frame_s']
t1v = trial1v.kinematics['frame_s']
t2v = trial2v.kinematics['frame_s']

lx1b, ly1b, rx1b, ry1b  = trial1b.kinematics['left_x'], trial1b.kinematics['left_y'], trial1b.kinematics['right_x'], trial1b.kinematics['left_x']
lx2b, ly2b, rx2b, ry2b  = trial2b.kinematics['left_x'], trial2b.kinematics['left_y'], trial2b.kinematics['right_x'], trial2b.kinematics['left_x']
lx1o, ly1o, rx1o, ry1o  = trial1o.kinematics['left_x'], trial1o.kinematics['left_y'], trial1o.kinematics['right_x'], trial1o.kinematics['left_x']
lx2o, ly2o, rx2o, ry2o  = trial2o.kinematics['left_x'], trial2o.kinematics['left_y'], trial2o.kinematics['right_x'], trial2o.kinematics['left_x']
lx1v, ly1v, rx1v, ry1v  = trial1v.kinematics['left_x'], trial1v.kinematics['left_y'], trial1v.kinematics['right_x'], trial1v.kinematics['left_x']
lx2v, ly2v, rx2v, ry2v  = trial2v.kinematics['left_x'], trial2v.kinematics['left_y'], trial2v.kinematics['right_x'], trial2v.kinematics['left_x']


fig, axs = plt.subplots(6,2, figsize=(15,10),sharey='row')#, sharex='col')#, sharey=True)
#Titles
names = ['a.1', 'b.1', 'a.2', 'b.2', 'a.3', 'b.3', 'a.4', 'b.4', 'a.5', 'b.5', 'a.6', 'b.6']
for i, ax in enumerate(axs.reshape(-1)):
    ax.set_title(names[i], loc='center', fontsize='large', fontweight='bold')
    ax.set_yticks(range(1), fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=14)

# A 1
axs[0,0].plot(t1b,ly1b,c='k'), axs[0,0].plot(t1b,ry1b, c='gray', linestyle = '--'), axs[0,0].set_ylabel('HandsY (m)', fontsize=17)#, axs[0,0].set_ylim(0, 0.6),     axs[0,0].set_yticks([0, 0.3, 0.6])
axs[1,0].plot(t1b,lx1b,c='k'), axs[1,0].plot(t1b,rx1b, c='gray', linestyle = '--'), axs[1,0].set_ylabel('HandsX (m)', fontsize=17)#, axs[1,0].set_ylim(-0.2, 0.2),  axs[1,0].set_yticks([-0.2, 0, 0.2])
# A 2
axs[2,0].plot(t1o,ly1o,c='k'), axs[2,0].plot(t1o,ry1o, c='gray', linestyle = '--'), axs[2,0].set_ylabel('HandsY (m)', fontsize=17)#, axs[2,0].set_ylim(0, 1), axs[2,0].set_yticks([0, 0.5, 1])
axs[3,0].plot(t1o,lx1o,c='k'), axs[3,0].plot(t1o,ry1o, c='gray', linestyle = '--'), axs[3,0].set_ylabel('HandsX (m)', fontsize=17)#, axs[3,0].set_ylim(-0.5, 0.5), axs[3,0].set_yticks([-0.5, 0, 0.5])
# A 3 
axs[4,0].plot(t1v,ly1v,c='k'), axs[4,0].plot(t1v,ry1v, c='gray', linestyle = '--'), axs[4,0].set_ylabel('HandsY (m)', fontsize=17)#, axs[4,0].set_ylim(0.2, 0.4), axs[4,0].set_yticks([0.2, 0.3, 0.4])
axs[5,0].plot(t1v,lx1v,c='k'), axs[5,0].plot(t1v,ry1v, c='gray', linestyle = '--'), axs[5,0].set_ylabel('HandsX (m)', fontsize=17)#, axs[5,0].set_ylim(-0.21, 0), axs[5,0].set_yticks([-0.2, -0.1, 0]),  axs[5,0].set_xlabel('Time (s)', fontsize=17)

# B 1
axs[0,1].plot(t2b,ly2b,c='k'), axs[0,1].plot(t2b,ry2b, c='gray', linestyle = '--')
axs[1,1].plot(t2b,lx2b,c='k'), axs[1,1].plot(t2b,rx2b, c='gray', linestyle = '--')
# B 2
axs[2,1].plot(t2o,ly2o,c='k'), axs[2,1].plot(t2o,ry2o, c='gray', linestyle = '--')
axs[3,1].plot(t2o,lx2o,c='k'), axs[3,1].plot(t2o,ry2o, c='gray', linestyle = '--')
# A 3 
axs[4,1].plot(t2v,ly2v,c='k'), axs[4,1].plot(t2v,ry2v, c='gray', linestyle = '--')
axs[5,1].plot(t2v,lx2v,c='k'), axs[5,1].plot(t2v,ry2v, c='gray', linestyle = '--'), axs[5,1].set_xlabel('Time (s)', fontsize=17)

#plt.text(0.5, 0.5, 'matplotlib', horizontalalignment='center',verticalalignment='center')#, transform=axs[0,0].transAxes)

plt.tight_layout()
fig.align_ylabels()
plt.savefig('./paper/hands_AB.eps', format='eps')
plt.show()

print("Process finished -- %s seconds --" % round((time.time() - start_time),2))