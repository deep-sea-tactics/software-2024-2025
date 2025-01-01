import numpy as np
import matplotlib.pyplot as plt 

plt.figure().add_subplot(projection='2d')

plt.plot([1,2,3,4], [0, 100, 200, 500], [10, 20,30, -60])
plt.ylabel('some numbers')
plt.show()