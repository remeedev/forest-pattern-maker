import pygame

listOfTrees = open("export.txt").read()
if listOfTrees.split('\n')[-1] == "-1":
    1/0
current = int(listOfTrees.split("\n")[0])
listOfTrees = listOfTrees.split('\n')[5:]

screen = pygame.display.set_mode((800, 800))

cache = {}

pygame.font.init()
font = pygame.font.SysFont("consolas", 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current = 0 if current == 0 else current-1
            elif event.key == pygame.K_RIGHT:
                current = len(listOfTrees) if current == len(listOfTrees) else current + 1
            toWrite = open("export.txt", "r").read()
            toWrite = toWrite.split('\n')
            toWrite[0] = str(current)
            open("export.txt", "w").write("\n".join(toWrite))
    screen.fill((255, 255, 255))
    if current == len(listOfTrees):
        screen.fill((0, 255, 0))
    else:
        if listOfTrees[current] not in list(cache.keys()):
            cache[listOfTrees[current]] = pygame.image.load("./"+"/".join(listOfTrees[current].split(","))+".png")
            cache[listOfTrees[current]] = pygame.transform.scale(cache[listOfTrees[current]], (800, 800))
        screen.blit(cache[listOfTrees[current]], (0, 0))
    text = font.render(str(current), True, (0, 0, 0))
    screen.blit(text, (0, 0))
    pygame.display.update()
