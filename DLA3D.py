from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
from mpl_toolkits.mplot3d import Axes3D


def randomInRadius(radius, seedX, seedY, seedZ):
    theta = np.pi*random.random()
    phi = 2*np.pi*random.random()
    x = seedX + int(radius*np.cos(phi)*np.sin(theta))
    y = seedY + int(radius*np.sin(phi)*np.sin(theta))
    z = seedZ + int(radius*np.cos(theta))
    return [x, y, z]


def checkOutRadius(seed, p, radius):
    return np.sqrt((seed[0]-p[0])**2+(seed[1]-p[1])**2+(seed[2]-p[2])**2) > radius


def checkAround(location, envSize, mat, seed, radius):
    foundOtherParticles = False
    reachLimit = False
    outTheSphere = False
    x = location[0]
    y = location[1]
    z = location[2]
    if x-1 < 1 or x+1 > envSize-1 or y-1 < 1 or y+1 > envSize-1 or z-1 < 1 or z+1 > envSize-1:
        reachLimit = True
    if not reachLimit:
        front = mat[x-1, y, z]
        back = mat[x+1, y, z]
        left = mat[x, y-1, z]
        right = mat[x, y+1, z]
        down = mat[x, y, z-1]
        up = mat[x, y, z+1]

        if down == 1 or up == 1 or right == 1 or left == 1 or front == 1 or back == 1:
            foundOtherParticles = True

        if (checkOutRadius(seed, [x, y-1, z], radius) or
            checkOutRadius(seed, [x, y+1, z], radius) or
            checkOutRadius(seed, [x-1, y, z], radius) or
            checkOutRadius(seed, [x+1, y, z], radius) or
            checkOutRadius(seed, [x, y, z-1], radius) or
                checkOutRadius(seed, [x, y, z+1], radius)):
            outTheSphere = True

    if not foundOtherParticles and not reachLimit:
        p = random.random()
        if p < 1/6:
            location = [x-1, y, z]
        elif p < 1/3:
            location = [x+1, y, z]
        elif p < 1/2:
            location = [x, y-1, z]
        elif p < 2/3:
            location = [x, y+1, z]
        elif p < 5/6:
            location = [x, y, z-1]
        else:
            location = [x, y, z+1]
    return(location, foundOtherParticles, reachLimit, outTheSphere)


def DLA(radius, gif):

    if not os.path.isdir("images"):
        os.mkdir("images")
    if gif:
        import imageio

    envSize = radius*2+1
    seedX = radius
    seedY = radius
    seedZ = radius
    mat = np.zeros((envSize, envSize, envSize))
    mat[seedX][seedY][seedZ] = 1

    print(mat)

    colorMap = np.empty(mat.shape, dtype=object)
    print(mat.shape, colorMap)
    randomWalkerCount = 0
    isComplete = False
    addedCount = 0
    usedInterval = []
    while not isComplete:
        randomWalkerCount += 1
        random.seed()
        location = randomInRadius(
            radius=radius, seedX=seedX, seedY=seedY, seedZ=seedZ
        )

        foundOtherParticles = False
        reachLimit = False
        while not foundOtherParticles and not reachLimit:
            newLocation, foundOtherParticles, reachLimit, outTheSphere = checkAround(
                location=location, envSize=envSize, mat=mat, seed=[seedX, seedY, seedZ], radius=radius)

            if foundOtherParticles:
                print(foundOtherParticles,
                      location[0], location[1], location[2])
                mat[location[0], location[1], location[2]] = 1
                addedCount += 1
            else:
                location = newLocation

        intervalSavePic = range(0, 400000, 25)
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
                ax.voxels(mat, facecolor='red', edgecolor='yellow')
                # plt.cm.Blues) #ocean, Paired
                # plt.matshow(mat, interpolation='nearest', cmap=colorMap)
                # plt.xlabel("direction, $x$", fontsize=15)
                # plt.ylabel("direction, $y$", fontsize=15)
                plt.savefig(filename, dpi=200)
                plt.close()

        if randomWalkerCount == 400000:
            print("CAUTION: had to break the cycle, taking too many iterations")
            isComplete = True
        if foundOtherParticles and outTheSphere:
            print("Random walkers in the cluster: ", addedCount)
            isComplete = True

    plt.title("DLA Cluster", fontsize=20)
    # plt.cm.Blues) #ocean, Paired
    plt.figure()
    ax = plt.subplot(projection='3d')
    ax.voxels(mat, facecolor='red', edgecolor='yellow')
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
