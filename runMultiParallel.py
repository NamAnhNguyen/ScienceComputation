import numpy as np
import imageio
import os

import multiprocessing
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from MultiCoralVisualize import DLA


if not os.path.isdir("multicorals"):
    os.mkdir("multicorals")
envSize = 50
mat = np.zeros((envSize, envSize, envSize))
randomWalkerCount = 0
usedInterval = []
addedCount = 0


def doJob(i):
    DLA(mat, 5, True, randomWalkerCount, usedInterval, addedCount, envSize)


if __name__ == "__main__":

    pool = multiprocessing.Pool(processes=4)
    input = range(0, 100)
    result = pool.map(doJob, input)
    pool.close()
    pool.join
    # processed_list = Parallel(n_jobs=5, backend="threading")(
    #     delayed(doJob)(i) for i in range(0, 10))
    # if randomWalkerCount in range(0, 400000, 25):
    #     print("save picture")
    #     # append to the used count
    #     usedInterval.append(randomWalkerCount)
    #     label = str(randomWalkerCount)
    #     filename = "multicorals/cluster"+label+".png"
    #     # print(filename)
    #     plt.title("DLA Cluster", fontsize=20)
    #     plt.figure()
    #     ax = plt.subplot(projection='3d')
    #     ax.voxels(mat, facecolor='red', edgecolor='pink')
    #     # plt.cm.Blues) #ocean, Paired
    #     # plt.matshow(mat, interpolation='nearest', cmap=colorMap)
    #     # plt.xlabel("direction, $x$", fontsize=15)
    #     # plt.ylabel("direction, $y$", fontsize=15)
    #     plt.savefig(filename, dpi=200)
    #     plt.close()


with imageio.get_writer('multicorals/movie.gif', mode='I') as writer:
    for i in usedInterval:
        filename = "multicorals/cluster"+str(i)+".png"
        image = imageio.imread(filename)
        writer.append_data(image)
        os.remove(filename)
    # image = imageio.imread("multicorals/cluster.png")
    # writer.append_data(image)
