import pygame

pygame.init()

aspect_ratio = 1080/900
width = 800
height = width/aspect_ratio

gridSize = int(open("image.txt").read().split("\n")[0])
percentageCover = 0.9

top_aspect_ratio = 2

genScreen = pygame.Surface((width, height))
topImg = pygame.image.load("./grass/top.png")
topWidth = (width*percentageCover)/gridSize
topHeight = topWidth/top_aspect_ratio
topImg = pygame.transform.scale(topImg, (topWidth, topHeight))
leftImg = pygame.image.load("./grass/left.png")
rightImg = pygame.image.load("./grass/right.png")
sideWidth = (width*percentageCover)/(2*gridSize)
sideHeight = sideWidth*1.5
leftImg = pygame.transform.scale(leftImg, (sideWidth, sideHeight))
rightImg = pygame.transform.scale(rightImg, (sideWidth, sideHeight))

treePerc = 0.8

pos = [1, 1]

def convertPos(pos):
    addition = sum(pos)
    substraction = pos[0]-pos[1]
    outPos = []
    outPos.append(addition*(topWidth/2))
    outPos.append(substraction*(topHeight/2))
    startingX = (width-width*percentageCover)/2
    startingX += (topWidth*(1-treePerc)/2)
    startingY = (height/2)-topWidth*treePerc
    startingY += (topWidth*(1-treePerc)/2)
    outPos[0]+=startingX
    outPos[1]+=startingY
    return outPos

def understand_file(content):
    entries = content.split('\n')
    entries = entries[1:]
    plants = {}
    for entry in entries:
        splitted = entry.split(":")
        key = splitted[0]
        value = splitted[1]
        plants[key] = [str(x) for x in value.split(",")]
    return plants

def saveImg():
    pygame.image.save(genScreen, "out.png")

imgCache = {}

prev = ""

def updateScreen(screentoblit, postoblit):
    global prev
    if prev != open("image.txt").read():
        prev = open("image.txt").read()
        starterPosX = (width-width*percentageCover)/2
        starterPosY = (height/2)-(topHeight/2)
        genScreen.fill((34, 77, 60))
        for x in range(gridSize):
            genScreen.blit(leftImg, (starterPosX+sideWidth*x, starterPosY+(topHeight/2)*(x+1)))
        for x in range(gridSize):
            for y in range(gridSize):
                genScreen.blit(topImg, (starterPosX+(topWidth/2)*y, starterPosY+(topHeight/2)*y))
            starterPosX+=topWidth/2
            starterPosY -= topHeight/2
        for x in range(gridSize):
            genScreen.blit(rightImg, (starterPosX+sideWidth*x, (starterPosY+topHeight*(gridSize+0.5))-(topHeight/2)*(x+1)))
        trees = open("image.txt", "r").read()
        plants = understand_file(trees)
        for y in range(gridSize):
            for x in range(gridSize):
                posAsString = str(gridSize-1-x)+","+str(y)
                if posAsString in list(plants.keys()):
                    tree = plants[posAsString]
                    filePath = "./"+tree[0]+"/"+tree[1]+".png"
                    if filePath in list(imgCache.keys()):
                        image = imgCache[filePath]
                    else:
                        image = pygame.image.load(filePath)
                        image = pygame.transform.scale(image, (topWidth*treePerc, topWidth*treePerc))
                        imgCache[filePath] = image
                    genScreen.blit(image, convertPos((x, gridSize-1-y)))
    screentoblit.blit(genScreen, postoblit)
