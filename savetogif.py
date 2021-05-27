
from multiprocessing import Process, Array, Value, Lock
import os
from MultiCoralVisualizeParallel import DLA
import numpy as np
import imageio
import ctypes as c
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with imageio.get_writer('multicorals/movie.gif', mode='I') as writer:
    for i in range(0, 300, 50):
        if i != 0:
            filename = "multicorals/cluster"+str(i)+".png"
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)
image = imageio.imread("multicorals/cluster.png")
writer.append_data(image)
