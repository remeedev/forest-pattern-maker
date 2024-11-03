import pixelize, pygame, math

imgSource = input("Enter image name: ")
imgSize = int(input('Enter side size for image: '))
imgMultiplier = 1.5
ogImg = pygame.image.load(imgSource)
size = min(ogImg.get_size())
img = pygame.Surface((size, size))
img.blit(ogImg, (0, 0))
pygame.image.save(img, imgSource)

pixelize.pixel(imgSource,"out.png", imgSize)

import json
colors = json.loads(open("colors.json").read())

def get_similar_color(color):
    tree = ""
    minDiff = 260
    colorMin = []
    for check in list(colors.keys()):
        check = [int(s) for s in check.split(" ")]
        diff = math.sqrt((check[0]-color[0])**2 + (check[1]-color[1])**2 + (check[1]-color[1])**2)
        if diff < minDiff:
            minDiff = diff
            colorMin = check
            tree = colors[" ".join([str(s) for s in check])]
    return [colorMin, tree]    
option = input("Try to match pixels (1)?\nLight based (2)")
if option == '2':
    def umbral(img:str):
        outVal = []
        imgName = img
        img = pygame.image.load(img)
        avg = [0, 0, 0]
        count = 0
        outImg = pygame.Surface((imgSize, imgSize))
        for y in range(imgSize):
            for x in range(imgSize):
                color = img.get_at((x, y))
                avg[0] += color[0]
                avg[1] += color[1]
                avg[2] += color[2]
                count+=1
        avg[0] /= count
        avg[1] /= count
        avg[2] /= count
        avg = sum(avg)/len(avg)
        for y in range(imgSize):
            for x in range(imgSize):
                color = img.get_at((x, y))
                color = sum(color)/len(color)
                if color > avg*imgMultiplier - avg*imgMultiplier*0.2 and color < avg*imgMultiplier + avg*imgMultiplier*0.2:
                    pygame.draw.rect(outImg, (100, 100, 100), (x, y, 1, 1))
                elif color > avg*imgMultiplier + avg*imgMultiplier*0.2:
                    pygame.draw.rect(outImg, (255, 255, 255), (x, y, 1, 1))
        return outImg          

    processImg = umbral("out.png")
    processImg = pygame.transform.scale(processImg, (800, 800))

    screen = pygame.display.set_mode((800, 800))
    done = False
    pygame.font.init()
    font = pygame.font.SysFont('consolas',32)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEWHEEL:
                imgMultiplier += event.y*0.01
                processImg = umbral("out.png")
                processImg = pygame.transform.scale(processImg, (800, 800))
        screen.fill((255, 255, 255))
        text = font.render(str(imgMultiplier), True, (255, 0, 0))

        screen.blit(processImg, (0, 0))
        screen.blit(text, (0, 0))
        
        pygame.display.update()

    print("Multiplier set at", imgMultiplier)
    processImg = umbral("out.png")
    out = str(imgSize)
    for y in range(imgSize):
        for x in range(imgSize):
            out+="\n" + str(imgSize-1-y) + "," + str(imgSize-1-x) + ":"
            if processImg.get_at((x, y)) == (255, 255, 255, 255):
                out+="99,4"
            elif processImg.get_at((x, y)) == (100, 100, 100, 255):
                out+="74,4"
            else:
                out+="0,4"

    open("image.txt", "w").write(out)
elif option == "1":
    imgtocheck = pygame.image.load("out.png")
    out = str(imgSize)
    outImg = pygame.Surface((imgSize, imgSize))
    for y in range(imgSize):
        for x in range(imgSize):
            out+="\n" + str(imgSize-1-y) + "," + str(imgSize-1-x) + ":"
            colorInfo = get_similar_color(imgtocheck.get_at((x, y)))
            pygame.draw.rect(outImg, colorInfo[0], (x, y, 1, 1))
            out+=colorInfo[1]
    pygame.image.save(outImg, "out.png")
    open("image.txt", "w").write(out)
    
import program
