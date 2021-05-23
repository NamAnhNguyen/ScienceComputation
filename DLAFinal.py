from hashlib import new
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
from mpl_toolkits.mplot3d import Axes3D


def randomInCubic(size):
    direction = random.random()
    location = []
    if direction < 1/6:  # L
        location = [int(random.random()*size), int(random.random()*size), size]
    elif direction < 1/3:  # R
        location = [int(random.random()*size), int(random.random()*size), 0]

    elif direction < 1/2:  # B
        location = [0, int(random.random()*size), int(random.random()*size)]
    elif direction < 2/3:  # F
        location = [size, int(random.random()*size), int(random.random()*size)]

    elif direction < 5/6:  # U
        location = [int(random.random()*size), 0, int(random.random()*size)]
    else:  # D
        location = [int(random.random()*size), size, int(random.random()*size)]

    print("location:", location)
    return location, direction


def checkAround(location, envSize, mat, direction):
    foundOtherParticles = False
    reachLimit = False
    x = location[0]
    y = location[1]
    z = location[2]
    if x-1 < 0 or x+1 > envSize or y-1 < 0 or y+1 > envSize or z-1 < 0 or z+1 > envSize:
        reachLimit = True
    if not reachLimit:
        tmp1 = random.random()
        tmp2 = random.random()

        if direction < 1/6:
            if tmp1 < 0.5:
                newZ = z-1
            if tmp2 > 0.8:
                newX = x+1
            elif tmp2 > 0.6:
                newX = x-1
            elif tmp2 > 0.4:
                newY = y+1
            elif tmp2 > 0.2:
                newY = y-1
        elif direction < 1/3:
            if tmp1 < 0.5:
                newZ = z+1
            if tmp2 > 0.8:
                newX = x+1
            elif tmp2 > 0.6:
                newX = x-1
            elif tmp2 > 0.4:
                newY = y+1
            elif tmp2 > 0.2:
                newY = y-1
        elif direction < 1/2:
            if tmp1 < 0.5:
                newX = x+1
            if tmp2 > 0.8:
                newZ = z+1
            elif tmp2 > 0.6:
                newZ = z-1
            elif tmp2 > 0.4:
                newY = y+1
            elif tmp2 > 0.2:
                newY = y-1
        elif direction < 2/3:
            if tmp1 < 0.5:
                newX = x-1
            if tmp2 > 0.8:
                newZ = z+1
            elif tmp2 > 0.6:
                newZ = z-1
            elif tmp2 > 0.4:
                newY = y+1
            elif tmp2 > 0.2:
                newY = y-1
        elif direction < 5/6:
            if tmp1 < 0.5:
                newY = y+1
            if tmp2 > 0.8:
                newX = x+1
            elif tmp2 > 0.6:
                newX = x-1
            elif tmp2 > 0.4:
                newZ = z+1
            elif tmp2 > 0.2:
                newZ = z-1
        else:
            if tmp1 < 0.5:
                newY = y-1
            if tmp2 > 0.8:
                newX = x+1
            elif tmp2 > 0.6:
                newX = x-1
            elif tmp2 > 0.4:
                newZ = z+1
            elif tmp2 > 0.2:
                newZ = z-1

    # print("new location", [newX, newY, newZ])
    return([newX, newY, newZ], foundOtherParticles, reachLimit)


def DLA(size, gif):

    if not os.path.isdir("images"):
        os.mkdir("images")
    if gif:
        import imageio

    envSize = size*2+1
    seedX = size
    seedY = size
    seedZ = size
    mat = np.zeros((envSize, envSize, envSize))
    mat[seedX][seedY][seedZ] = 1
    print(mat)

    randomWalkerCount = 0
    isComplete = False
    addedCount = 0
    usedInterval = []
    while not isComplete:
        randomWalkerCount += 1
        random.seed()
        location, direction = randomInCubic(
            size=envSize
        )

        foundOtherParticles = False
        reachLimit = False
        while not foundOtherParticles and not reachLimit:
            newLocation, foundOtherParticles, reachLimit = checkAround(
                location=location, envSize=envSize, mat=mat, direction=direction)
            if foundOtherParticles:
                print(foundOtherParticles,
                      location[0], location[1], location[2])
                mat[location[0], location[1], location[2]] = 1
                addedCount += 1
            else:
                print("not found + reachLimit:", reachLimit)
                location = newLocation

        intervalSavePic = range(0, 10000, 50)
        if randomWalkerCount in intervalSavePic:
            print("still working, have added ", randomWalkerCount,
                  " random walkers.", " Added to cluster: ", addedCount)
        if gif:
            if randomWalkerCount in intervalSavePic:
                print("save picture")
                # append to the used count
                usedInterval.append(randomWalkerCount)
                label = str(randomWalkerCount)
                filename = "images/cluster"+label+".png"
                # print(filename)
                plt.title("DLA Cluster", fontsize=20)
                plt.figure()
                ax = plt.subplot(projection='3d')
                ax.voxels(mat)
                # plt.cm.Blues) #ocean, Paired
                # plt.matshow(mat, interpolation='nearest', cmap=colorMap)
                # plt.xlabel("direction, $x$", fontsize=15)
                # plt.ylabel("direction, $y$", fontsize=15)
                plt.savefig(filename, dpi=200)
                plt.close()

        if randomWalkerCount == 10000:
            isComplete = True
        if (foundOtherParticles & reachLimit):
            print("Random walkers in the cluster: ", addedCount)
            isComplete = True

    plt.title("DLA Cluster", fontsize=20)
    # plt.cm.Blues) #ocean, Paired
    plt.figure()
    ax = plt.subplot(projection='3d')
    ax.voxels(mat)
    # plt.ylabel("direction, $y$", fontsize=15)
    plt.savefig("images/cluster.png", dpi=200)
    plt.close()
    print(usedInterval)
    if gif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in usedInterval:
                filename = "images/cluster"+str(i)+".png"
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
            image = imageio.imread("images/cluster.png")
            writer.append_data(image)

    return(addedCount, mat)
