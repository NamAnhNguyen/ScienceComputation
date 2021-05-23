from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
from mpl_toolkits.mplot3d import Axes3D


def randomInRadius(radius, seedX, seedY):
    theta_angle = 2*np.pi*random.random()
    x = seedX + int(radius*np.cos(theta_angle))
    y = seedY + int(radius*np.sin(theta_angle))
    return [x, y]


def checkAround(location, envSize, mat):
    foundOtherParticles = False
    reachLimit = False
    outTheSphere = False
    x = location[0]
    y = location[1]
    if x-1 < 1 or x+1 > envSize-1 or y-1 < 1 or y+1 > envSize-1:
        reachLimit = True
    if not reachLimit:
        down = mat[x, y-1]
        up = mat[x, y+1]
        left = mat[x-1, y]
        right = mat[x+1, y]

        if down == 1 or up == 1 or right == 1 or left == 1:
            foundOtherParticles = True

        if down == 2 or up == 2 or right == 2 or left == 2:
            outTheSphere = True

    if not foundOtherParticles and not reachLimit:
        p = random.random()
        if p < 1/4:
            location = [x-1, y]
        elif p < 1/2:
            location = [x+1, y]
        elif p < 3/4:
            location = [x, y-1]
        else:
            location = [x, y+1]
    return(location, foundOtherParticles, reachLimit, outTheSphere)


def DLA(radius, gif):

    if not os.path.isdir("images"):
        os.mkdir("images")
    if gif:
        import imageio
    
    envSize = radius*2 + 5
    seedX = radius
    seedY = radius
    mat = np.zeros((envSize, envSize))
    print(mat)
    for i in range(0, envSize):
        for j in range(0, envSize):
            if i == seedX and j == seedY:
                mat[i][j] = 1
            elif np.sqrt((seedX-i)**2+(seedY-j)**2) > radius:
                mat[i][j] = 2
    colorMap = colors.ListedColormap(['red', 'green', 'blue'])
    randomWalkerCount = 0
    isComplete = False
    addedCount = 0
    usedInterval = []
    while not isComplete:
        print(randomWalkerCount)
        randomWalkerCount += 1
        random.seed()
        location = randomInRadius(
            radius=radius, seedX=seedX, seedY=seedY
        )

        foundOtherParticles = False
        reachLimit = False
        while not foundOtherParticles and not reachLimit:
            newLocation, foundOtherParticles, reachLimit, outTheSphere = checkAround(
                location=location, envSize=envSize, mat=mat)
            if foundOtherParticles:
                mat[location[0], location[1]] = 1
                addedCount += 1
            else:
                location = newLocation

        intervalSavePic = range(0, 400000, 20)
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
                print(filename)
                plt.title("DLA Cluster", fontsize=20)
                # plt.cm.Blues) #ocean, Paired
                plt.matshow(mat, interpolation='nearest', cmap=colorMap)
                plt.xlabel("direction, $x$", fontsize=15)
                plt.ylabel("direction, $y$", fontsize=15)
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
    plt.matshow(mat, interpolation='nearest', cmap=colorMap)
    plt.xlabel("direction, $x$", fontsize=15)
    plt.ylabel("direction, $y$", fontsize=15)
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
