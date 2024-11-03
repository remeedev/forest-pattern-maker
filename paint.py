import pygame, json, generator

colorScreen = pygame.Surface((800, 200))

size = int(open("image.txt").read().split("\n")[0])

colors = json.loads(open("colors.json").read())
colorNum = 0
colorList = []
squareSize = 16
for color in list(colors.keys()):
    pygame.draw.rect(colorScreen, [int(s) for s in color.split(" ")], ((squareSize*(colorNum%(800/squareSize)), int(colorNum*squareSize/800)*squareSize), (squareSize, squareSize)))
    colorList.append([int(s) for s in color.split(" ")])
    colorNum +=1

selectedColor = ()

drawn = generator.understand_file(open("image.txt").read())
invertedcolors = {v: k for k, v in colors.items()}

for k, v in drawn.items():
    drawn[k] = [int(s) for s in invertedcolors[",".join(v)].split(' ')]

paintScreen = pygame.Surface((800, 1000))

def saveDrawn(drawn):
    text = str(size)+"\n"
    for key in list(drawn.keys()):
        text+= key+":"+colors[" ".join([str(s) for s in drawn[key]])]+"\n"
    text = text[:-1]
    open("image.txt", "w").write(text)

drawing = False
deleting = False

def processEvents(event):
    global drawn, selectedColor
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        if pos[1] > 800:
            x = int(pos[0]/squareSize)
            y = int((pos[1]-800)/squareSize)
            index = int(x + y*(800/squareSize))
            if index < len(colorList):
                selectedColor = colorList[index]
    elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if pos[1] <= 800:
            x = int(pos[0]/(800/size))
            y = int((pos[1])/(800/size))
            if selectedColor != () and pygame.mouse.get_pressed()[0]:
                drawn[str(size-1-y) + "," + str(size-1-x)] = selectedColor
            elif pygame.mouse.get_pressed()[2] and str(size-1-y) + "," + str(size-1-x) in list(drawn.keys()):
                del drawn[str(size-1-y) + "," + str(size-1-x)]
            elif pygame.mouse.get_pressed()[1] and str(size-1-y) + "," + str(size-1-x) in list(drawn.keys()):
                selectedColor = drawn[str(size-1-y) + "," + str(size-1-x)]
            saveDrawn(drawn)
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE and selectedColor != ():
            pos = pygame.mouse.get_pos()
            x = int(pos[0]/(800/size))
            y = int((pos[1])/(800/size))
            filling = True
            firstRemoved = ()
            if str(size-1-y) + "," + str(size-1-x) in list(drawn.keys()):
                firstRemoved = drawn[str(size-1-y) + "," + str(size-1-x)]
            added = {str(size-1-y) + "," + str(size-1-x):selectedColor}
            drawn[str(size-1-y) + "," + str(size-1-x)] = selectedColor
            while filling:
                filling = False
                _added = dict(added)
                for pos in _added.keys():
                    for _x in range(-1, 2):
                        for _y in range(-1, 2):
                            if int(pos.split(",")[0])+_x < 0 or int(pos.split(",")[0])+_x >= size or int(pos.split(",")[1])+_y < 0 or int(pos.split(",")[1])+_y >= size:
                                continue
                            positionChecked = str(int(pos.split(",")[0])+_x) + "," + str(int(pos.split(",")[1])+_y)
                            if positionChecked not in list(drawn.keys()):
                                added[positionChecked] = selectedColor
                                drawn[positionChecked] = selectedColor
                                filling = True
                            elif drawn[positionChecked] != selectedColor and drawn[positionChecked] == firstRemoved:
                                added[positionChecked] = selectedColor
                                drawn[positionChecked] = selectedColor
                                filling = True
                    del added[pos]
            saveDrawn(drawn)
    if event.type in [pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
        updatePaint()

def updatePaint():
    paintScreen.fill((255, 255, 255))
    for square in list(drawn.keys()):
        coords = square.split(",")
        coords = [size-1-int(coords[1]), size-1-int(coords[0])]
        pos = [int(s)*(800/size) for s in coords]
        pygame.draw.rect(paintScreen, drawn[square], (pos, (800/size, 800/size)))
    paintScreen.blit(colorScreen, (0, 800))

updatePaint()

def updateScreen(screenToBlit, postoblit):
    mouseScreen = pygame.Surface((800, 1000))
    mouseScreen.blit(paintScreen, (0, 0))
    if selectedColor != ():
        pos = pygame.mouse.get_pos()
        if pos[1] < 800:
            pygame.draw.rect(mouseScreen, selectedColor, ((int(pos[0]/(800/size))*(800/size), int((pos[1])/(800/size))*(800/size)), (800/size, 800/size)))
    screenToBlit.blit(mouseScreen, postoblit)
