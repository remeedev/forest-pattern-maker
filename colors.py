import pygame
import os


def all():
    colors = {}
    for folder in range(104):
        for file in os.listdir("./"+str(folder)):
            image = pygame.image.load("./" + str(folder) + "/"+file)
            r=0
            g=0
            b=0
            pixels = 0
            for y in range(image.get_height()):
                for x in range(image.get_width()):
                    color = image.get_at((x, y))
                    if color[3] != 0:
                        pixels+=1
                        r+=color[0]
                        g+=color[1]
                        b+=color[2]

            r/=pixels
            g/=pixels
            b/=pixels
            r = int(r)
            g = int(g)
            b = int(b)
            key = " ".join([str(s) for s in [r, g, b]])
            colors[key] = str(folder)+","+file.split(".")[0]
    return colors

def possible():
    colors = {}
    for folder in range(104):
        iterable = os.listdir("./"+str(folder))
        if len(iterable) > 4:
            iterable = iterable[-4]
        else:
            iterable = iterable[-1]
        iterable = [iterable]
        for file in iterable:
            image = pygame.image.load("./" + str(folder) + "/"+file)
            r=0
            g=0
            b=0
            pixels = 0
            for y in range(image.get_height()):
                for x in range(image.get_width()):
                    color = image.get_at((x, y))
                    if color[3] != 0:
                        pixels+=1
                        r+=color[0]
                        g+=color[1]
                        b+=color[2]

            r/=pixels
            g/=pixels
            b/=pixels
            r = int(r)
            g = int(g)
            b = int(b)
            key = " ".join([str(s) for s in [r, g, b]])
            colors[key] = str(folder)+","+file.split(".")[0]
    return colors
colors = possible()
import json

print(colors)

open("colors.json", "w").write(json.dumps(colors))
