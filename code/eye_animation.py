#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

results = pd.read_csv("../files/Object Hit - [Child - practice] - RIGHT - 12_02.csv",encoding= 'unicode_escape', sep=',',skiprows = 390, parse_dates=[0,1,2])

gazeX = results['Gaze_X']
gazeY = results['Gaze_Y']
time = results['Frame time (s)']
time = [str(round(i, 4)) for i in time]

def plot_animation():
    fig, ax = plt.subplots()
    def animate(i):
        ax.plot(gazeX[i], gazeY[i], 'ro')
        ax.set_title(time[i] + ' ms')
        #ax.set_title(time[i])
        ax.set_xlim([-0.5,0.5])
        ax.set_ylim([0,1])

    anim = FuncAnimation(fig, animate, frames=len(gazeX), interval=5, repeat=False)
    plt.show()

    # save
    f = r"./animate_func.gif"
    anim.save(f, fps=30)
def plot_static():
    fig = plt.figure(figsize=(8,5))
    plt.xlim([-0.5,0.5])
    plt.ylim([0,1])
    i = 0
    while i < len(gazeX):
        plt.plot(gazeX[i],gazeY[i],'ro')
        i+=1
    plt.show()

plot_animation()
plot_static()

