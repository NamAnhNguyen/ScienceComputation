from multiprocessing import Process, Array, Value, Lock
import os
from MultiCoralVisualizeParallel import DLA
import numpy as np
import imageio
import ctypes as c
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


if not os.path.isdir("multicorals"):
    os.mkdir("multicorals")

envSize = 50
matSize = envSize * envSize * envSize
print(matSize)
mat = Array(c.c_int64, matSize)
randomWalkerCount = Value('i', 0)
usedInterval = Array(c.c_int64, 10000)
addedCount = Value('i', 0)

if __name__ == '__main__':
    lock = Lock()
    procs = [Process(target=DLA, args=(mat, 5, True, randomWalkerCount,
                                       usedInterval, addedCount, envSize, lock))
             for i in range(10)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    ThreeD_mat = np.frombuffer(mat.get_obj())
    ThreeD_mat = ThreeD_mat.reshape(envSize, envSize, envSize)
    plt.title("DLA Cluster", fontsize=20)
    # plt.cm.Blues) #ocean, Paired
    plt.figure()
    ax = plt.subplot(projection='3d')
    ax.voxels(ThreeD_mat, facecolor='red', edgecolor='pink')
    # plt.ylabel("direction, $y$", fontsize=15)
    plt.savefig("multicorals/cluster.png", dpi=200)
    plt.close()

    with imageio.get_writer('multicorals/movie.gif', mode='I') as writer:
        for i in usedInterval:
            if i != 0:
                filename = "multicorals/cluster"+str(i)+".png"
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
        image = imageio.imread("multicorals/cluster.png")
        writer.append_data(image)
