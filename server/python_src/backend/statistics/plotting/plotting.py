'''
Plotting system
Works using a Dictionary to contain plot objects (plotObject).
Each plot object is assigned a unique 'key' upon creation
plotObject can be retrived through this key using plotAt
Plots are updated with the tick function; each tick specifying what needs to be updated
Various functions can be run on a plotObject
'''

'''
Install if necessay:
pip install numpy
pip install matplotlib
'''

import numpy as np
import matplotlib.pyplot as plt 
import random
import frontend.dss.deep_seashell as dss
import time 

#General set up
plotID = 0
plotDict = {}
interval = 1
#plt.ion() #Interactive ON


def defaultFigData2D():
    return [[], []]

#Plot Object Class
class plotObject:
    key = ""
    storedID = 0
    '''
    Stored ID may seem to fill the sign role as the key; but storedID represents
    the internal numerical system matplotlib uses to track plots.
    Meanwhile, the key is the external way the user should use to track plots.
    '''
    figData = defaultFigData2D()
    projection_3d: bool

    #Initialization
    def __init__(self, key: str, projection_3d, x_axis, y_axis, z_axis, title):
        global plotID #This is necessary to keep track of an the internal method matplotlib keeps plots
        global plotDict #Dictionary that hoods plots

        #Sets internal ID stuff
        self.storedID = plotID
        plotID += 1

        self.projection_3d = projection_3d #Determines 3D mode
        self.key = key #Sets key (what the user refers to the plot)

        #Projection set-up
        if not projection_3d:
            self.figData = defaultFigData2D()
            fig2D = plt.figure(plotID)
        else:
            self.figData = [[], [], []]
            fig3D = plt.figure(plotID).add_subplot(projection='3d')
            fig3D.set_zlabel(z_axis)
        
        #Formatting and final key dictionary assignment
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        plotDict[key] = self

    #Default 2D Graph Declaration
    def default2D(key: str): 
        return plotObject(key, False, "X", "Y", "", key)
    
    #Default 3D Graph Declaration
    def default3D(key: str): 
        return plotObject(key, True, "X", "Y", "Z", key)

    #Get size
    def getDataSize(self):
        figDataSize = len(self.figData[0])
        return figDataSize
    
    #Getter at time
    def getDataAtTime(self, time: int):
        timeData = []
        timeData.append(self.figData[0][time])
        timeData.append(self.figData[1][time])
        if self.projection_3d:
            timeData.append(self.figData[2][time])
        return timeData
    
    #Returns average rate of change over whole interval
    def getDataAROC(self):
        #Currently broken
        AROC = 0
        first_point = self.getDataAtTime(0)
        second_point = self.getDataAtTime(self.getDataSize()-1)
        print(second_point)
        print(first_point)
        AROC = (second_point[1] - first_point[1])/(second_point[0] - first_point[0])
        return AROC

    def getDataIROC(self):
        #Currently broken
        pass

    def getDataArea(self):
        #Currently broken
        pass

    #Setter at time
    def setDataAtTime(self, time: int, new_x = 0, new_y = 0, new_z = 0):
       self.figData[0][time] = new_x
       self.figData[1][time] = new_y
       if self.projection_3d:
           self.figData[2][time] = new_z

    #Full report with stylization
    def reportAtTime(self, time: int):
        print("Current Plot: " + self.key)
        print("Time interval: " + str(time) + "/" + str(self.getDataSize()))
        print("Position: " + str(self.getDataAtTime(time)))
        print("-------------------------")


#Get object out of plotDict
def plotAt(key: str) -> plotObject | None:
    try:
        return (plotDict[key])
    except KeyError:
        return None

''''
Tick, updates a graph
Dynamically adpatable with optional x, y, and z inputs 
'''
def tick(key, x = None, y = None, z = None):
    if plotAt(key) == None:
        return

    figureID = plotAt(key).storedID
    data = plotAt(key).figData
    projection_3d = plotAt(key).projection_3d
    plt.figure(figureID)

    # X Inputs
    if x != None:
        data[0].append(x) #Y-Data (The actual data)
    else:
        prev_time = data[0][len(plotAt(key).figData[0])-1] #Log previous time
        data[0].append(prev_time + interval) #X-Data (Previous time + tick interval)
    
    # Y Inputs
    if y != None:
        data[1].append(y) #Y
    else: 
        data[1].append(0)

    # Z Inputs
    if z != None:
        data[2].append(z) #Z
    else:
        if projection_3d == True:
            data[2].append(0)
    
    # Final report
    # if projection_3d == False:
        # plt.plot(data[0], data[1]) 
    # else:
        # plt.plot(data[0], data[1], data[2]) 

NAMESPACE = "plotting::"
FILE_EXT = ".png"
class PlottingDSS:
    def cmd_plot_def(args: list[str]):
        MINIMUM_ARGS = 1
        if len(args) < MINIMUM_ARGS: return 1

        plotObject.default2D(args[0])
        return 0
    
    def cmd_plot_entry(args: list[str]):
        MINIMUM_ARGS = 3
        if len(args) < MINIMUM_ARGS: return 1

        found = plotAt(args[0])
        if found == None: return 1

        try:
            tick(args[0], float(args[1]), float(args[2]))
        except (ValueError, TypeError):
            return 1
        
        return 0
    
    def cmd_render(args: list[str]):
        MINIMUM_ARGS = 5
        if len(args) < MINIMUM_ARGS: return 1

        found = plotAt(args[0])
        if found == None: return 1

        plt.xlabel(args[1])
        plt.ylabel(args[2])
        plt.title(args[3])
        plt.scatter(found.figData[0], found.figData[1], linewidths=MARKER_WIDTH)
        plt.savefig(args[4] + FILE_EXT)
    
    def _define_all(_args):
        dss.Define.define(
            PlottingDSS.cmd_plot_def,
            NAMESPACE + "pltdef",
            """
            Defines a plot.

            Arguments: <name>
            """
        )

        dss.Define.define(
            PlottingDSS.cmd_plot_entry,
            NAMESPACE + "pltentry",
            """
            Inserts an entry into a plot.

            Arguments: <plot name> <x> <y>
            """
        )

        dss.Define.define(
            PlottingDSS.cmd_render,
            NAMESPACE + "pltrender",
            """
            Renders the plot to file.

            Arguments: <plot name> <x label> <y label> <title> <file name>
            """
        )

        
FIGURE_NAME = "res.png"
MARKER_WIDTH = 10.0

def init():
    dss.Define.additional_second_pass_commands.connect(PlottingDSS._define_all)

#Test stuff
if __name__ == "__main__":
    PLOT = "MATE Floats! Data"
    plotObject.default2D(PLOT)
    tick(PLOT, x=0, y=40)
    tick(PLOT, x=2, y=50)
    tick(PLOT, x=4, y=70)
    plt.xlabel("Thyme")
    plt.ylabel("Death")
    plt.title("Goofy Goober Rock")
    plt.scatter(plotAt(PLOT).figData[0], plotAt(PLOT).figData[1], linewidths=MARKER_WIDTH)
    plt.savefig("res.png")

    exit()
    plotObject.default2D("KEY2D")
    plotObject("KEY2D2", False, "guaca", "mole", "", "this me gauc")
    plotObject.default3D("KEY3D")
    plotObject.default3D("guacamole")

    for i in range(100):
        tick("KEY2D", x=4, y=random.randrange(-1000, -500))
        tick("KEY2D2", y=random.randrange(-1000, -500))
        tick("KEY3D", z=45)
        tick("guacamole", x=random.randrange(-1000, -500), z=random.randrange(-10, 50))
        #plotAt("guacamole").reportAtTime(i)

    plotAt("KEY2D2").reportAtTime(10)
    plotAt("KEY2D2").reportAtTime(plotAt("KEY2D2").getDataSize()-1)
    plotAt("KEY2D2").setDataAtTime(10, 1, 1000, 1000)
    plotAt("KEY2D2").reportAtTime(10)
    plotAt("KEY2D2").reportAtTime(plotAt("KEY2D2").getDataSize()-1)

    tick("KEY2D2")

    print(plotAt("KEY2D2").getDataAROC())
