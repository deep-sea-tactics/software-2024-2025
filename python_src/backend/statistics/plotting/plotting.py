import sys
if not ('numpy' in sys.modules and 'matplotlib' in sys.modules):
    !{sys.executable} -m pip install numpy
    !{sys.executable} -m pip install matplotlib

import numpy as np
import matplotlib.pyplot as plt 
import random

plt.ion() #Interactive ON
fig2D = plt.figure().add_subplot()
fig3D = plt.figure().add_subplot(projection='3d')

fig2D.set_xlabel('X')
fig2D.set_ylabel('Y')
fig3D.set_xlabel('X')
fig3D.set_ylabel('Y')
fig3D.set_zlabel('Z')

fig2DData = [[0], [0]]
fig3DData = [[0], [0], [0]]
interval = 1

def tick():
    tick_2d(random.randrange(0, 5))
    tick_3d(random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 5))

def tick_2d(data_input):
    prev_time = fig2DData[0][len(fig2DData[0])-1] #Log previous time
    fig2DData[0].append(prev_time + interval) #X-Data (Previous time + tick interval)
    fig2DData[1].append(data_input) #Y-Data (The actual data)
    fig2D.plot(fig2DData[0], fig2DData[1]) 

def tick_3d(x_input, y_input, z_input):
    fig3DData[0].append(x_input)
    fig3DData[1].append(y_input)
    fig3DData[2].append(z_input)
    fig3D.plot(fig3DData[0], fig3DData[1], fig3DData[2])

for i in range(100):
    tick()
