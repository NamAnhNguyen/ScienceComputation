import numpy as np
import imageio
import os

from MultiCoralVisualize import DLA


if not os.path.isdir("multicorals"):
    os.mkdir("multicorals")
envSize = 50
mat = np.zeros((envSize, envSize, envSize))
randomWalkerCount = 0
usedInterval = []
addedCount = 0
for i in range(0, 100):
    print("run in i =  ", i)
    mat, randomWalkerCount, usedInterval, addedCount = DLA(mat, 5, True, randomWalkerCount,
                                                           usedInterval, addedCount, envSize)

with imageio.get_writer('multicorals/movie.gif', mode='I') as writer:
    for i in usedInterval:
        filename = "multicorals/cluster"+str(i)+".png"
        image = imageio.imread(filename)
        writer.append_data(image)
        os.remove(filename)
    image = imageio.imread("multicorals/cluster.png")
    writer.append_data(image)
