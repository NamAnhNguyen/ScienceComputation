from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
from mpl_toolkits.mplot3d import Axes3D


def randomInRadius(radius, seedX, seedY, seedZ):
    theta = 0.5*np.pi*random.random()
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

        xy1 = mat[x-1, y-1, z]
        xy2 = mat[x-1, y+1, z]
        xy3 = mat[x+1, y-1, z]
        xy4 = mat[x+1, y+1, z]

        xz1 = mat[x-1, y, z-1]
        xz2 = mat[x-1, y, z+1]
        xz3 = mat[x+1, y, z-1]
        xz4 = mat[x+1, y, z+1]

        yz1 = mat[x, y-1, z-1]
        yz2 = mat[x, y+1, z+1]
        yz3 = mat[x, y-1, z-1]
        yz4 = mat[x, y+1, z+1]

        xyz1 = mat[x-1, y-1, z-1]
        xyz2 = mat[x-1, y-1, z+1]
        xyz3 = mat[x-1, y+1, z-1]
        xyz4 = mat[x-1, y+1, z+1]
        xyz5 = mat[x+1, y-1, z-1]
        xyz6 = mat[x+1, y-1, z+1]
        xyz7 = mat[x+1, y+1, z-1]
        xyz8 = mat[x+1, y+1, z+1]

        if (down == 1 or up == 1 or right == 1 or left == 1 or front == 1 or back == 1 or
           xy1 == 1 or xy2 == 1 or xy3 == 1 or xy4 == 1 or
           xz1 == 1 or xz2 == 1 or xz3 == 1 or xz4 == 1 or
           yz1 == 1 or yz2 == 1 or yz3 == 1 or yz4 == 1 or
           xyz1 == 1 or xyz2 == 1 or xyz3 == 1 or xyz4 == 1 or
           xyz5 == 1 or xyz6 == 1 or xyz7 == 1 or xyz8 == 1
                ):
            foundOtherParticles = True

        if (checkOutRadius(seed, [x, y-1, z], radius) or
            checkOutRadius(seed, [x, y+1, z], radius) or
            checkOutRadius(seed, [x-1, y, z], radius) or
            checkOutRadius(seed, [x+1, y, z], radius) or
            checkOutRadius(seed, [x, y, z-1], radius) or
            checkOutRadius(seed, [x, y, z+1], radius) or

            checkOutRadius(seed, [x-1, y-1, z], radius) or
            checkOutRadius(seed, [x-1, y+1, z], radius) or
            checkOutRadius(seed, [x+1, y-1, z], radius) or
            checkOutRadius(seed, [x+1, y+1, z], radius) or

            checkOutRadius(seed, [x-1, y, z-1], radius) or
            checkOutRadius(seed, [x-1, y, z+1], radius) or
            checkOutRadius(seed, [x+1, y, z-1], radius) or
            checkOutRadius(seed, [x+1, y, z-1], radius) or

            checkOutRadius(seed, [x, y-1, z-1], radius) or
            checkOutRadius(seed, [x, y-1, z+1], radius) or
            checkOutRadius(seed, [x, y+1, z-1], radius) or
            checkOutRadius(seed, [x, y+1, z+1], radius) or

            checkOutRadius(seed, [x-1, y-1, z-1], radius) or
            checkOutRadius(seed, [x-1, y-1, z+1], radius) or
            checkOutRadius(seed, [x-1, y+1, z-1], radius) or
            checkOutRadius(seed, [x-1, y+1, z+1], radius) or

                    checkOutRadius(seed, [x+1, y-1, z-1], radius) or
                    checkOutRadius(seed, [x+1, y-1, z+1], radius) or
                    checkOutRadius(seed, [x+1, y+1, z-1], radius) or
                    checkOutRadius(seed, [x+1, y+1, z+1], radius)
                ):
            outTheSphere = True

    if not foundOtherParticles and not reachLimit:
        p = random.random()
        if p < 1/26:
            location = [x, y-1, z]
        elif p < 2/26:
            location = [x, y+1, z]
        elif p < 3/26:
            location = [x-1, y, z]
        elif p < 4/26:
            location = [x+1, y, z]
        elif p < 5/26:
            location = [x, y, z-1]
        elif p < 6/26:
            location = [x, y, z+1]
        elif p < 7/26:
            location = [x-1, y-1, z]
        elif p < 8/26:
            location = [x-1, y+1, z]
        elif p < 9/26:
            location = [x+1, y-1, z]
        elif p < 10/26:
            location = [x+1, y+1, z]
        elif p < 11/26:
            location = [x-1, y, z-1]
        elif p < 12/26:
            location = [x-1, y, z+1]
        elif p < 13/26:
            location = [x+1, y, z-1]
        elif p < 14/26:
            location = [x+1, y, z+1]
        elif p < 15/26:
            location = [x, y-1, z-1]
        elif p < 16/26:
            location = [x, y-1, z+1]
        elif p < 17/26:
            location = [x, y+1, z-1]
        elif p < 18/26:
            location = [x, y+1, z+1]
        elif p < 19/26:
            location = [x-1, y-1, z-1]
        elif p < 20/26:
            location = [x-1, y-1, z+1]
        elif p < 21/26:
            location = [x-1, y+1, z-1]
        elif p < 22/26:
            location = [x-1, y+1, z+1]
        elif p < 23/26:
            location = [x+1, y-1, z-1]
        elif p < 24/26:
            location = [x+1, y-1, z+1]
        elif p < 25/26:
            location = [x+1, y+1, z-1]
        else:
            location = [x+1, y+1, z+1]
    return(location, foundOtherParticles, reachLimit, outTheSphere)


def DLA(mat, radius, gif, randomWalkerCount, usedInterval, addedCount, envSize):
    print("randomWalkerCount, usedInterval, addedCount, envSize"),
    print(randomWalkerCount, " ", usedInterval, " ", addedCount, " ", envSize)
    random.seed()
    # envSize = radius*2+1
    seedX = int(random.random() * envSize)
    seedY = int(random.random() * envSize)
    seedZ = 2
    mat[seedX][seedY][seedZ] = 1

    isComplete = False
    while not isComplete:
        randomWalkerCount += 1

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
                filename = "multicorals/cluster"+label+".png"
                # print(filename)
                plt.title("DLA Cluster", fontsize=20)
                plt.figure()
                ax = plt.subplot(projection='3d')
                ax.voxels(mat, facecolor='red', edgecolor='pink')
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
    ax.voxels(mat, facecolor='red', edgecolor='pink')
    # plt.ylabel("direction, $y$", fontsize=15)
    plt.savefig("multicorals/cluster.png", dpi=200)
    plt.close()
    print(usedInterval)

    return(mat, randomWalkerCount, usedInterval, addedCount)
