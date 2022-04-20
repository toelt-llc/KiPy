#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

results = pd.read_csv("../../files/Object_Hit_-_[Child_-_practice]_-_RIGHT_-_12_02.csv",encoding= 'unicode_escape', sep=',',skiprows = 390, parse_dates=[0,1,2])

gazeX = results['Gaze_X']
gazeY = results['Gaze_Y']
rightX = results['Right: Hand position X']
rightY = results['Right: Hand position Y']
#rightSpeed = results['Right: Hand speed']
leftX = results['Left: Hand position X']
leftY = results['Left: Hand position Y']
#leftSpeed = results['Left: Hand speed']
time = results['Frame time (s)']
time = [int(round(i, 4)) for i in time]

def plot_animation():
    fig, ax = plt.subplots()
    def animate(i):
        ax.plot(rightX[i],rightY[i],'ro')
        ax.plot(leftX[i],leftY[i],'bo')
        ax.plot(gazeX[i],gazeY[i],'go')
        if time[i] % 1 == 0:
            ax.set_title(str(time[i]) + ' ms')
        ax.set_xlim([-0.5,0.5])
        ax.set_ylim([0,1])

    anim = FuncAnimation(fig, animate, frames=int(len(gazeX)/4), interval=5, repeat=False)
    plt.show()
    #save
    f = r"./animate_func_all.gif"
    #anim.save(f, fps=30)
    plt.close()


def plot_static():
    fig = plt.figure(figsize=(8,5))
    plt.xlim([-0.5,0.5])
    plt.ylim([0,1])

    plt.plot(rightX,rightY,'ro', label='right')
    plt.plot(leftX,leftY,'bo', label='left')
    plt.plot(gazeX,gazeY,'go', label='gaze')

    plt.legend()
    plt.show()

plot_animation()
#plot_static()

