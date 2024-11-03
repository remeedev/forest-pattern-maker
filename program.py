import pygame, paint, generator

screen = pygame.display.set_mode((1600, 1000))
clock = pygame.time.Clock()

def clear():
    paint.drawn = {}
    paint.saveDrawn({})

clearButton = pygame.Rect((900, 700), (200, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            generator.saveImg()
            contents = open("image.txt").read()
            text = "0\nsize: " + contents.split("\n")[0] + "x" + contents.split("\n")[0]
            text+='\nTime per tree: 10min'
            totalTrees = int(contents.split("\n")[0])**2
            time = totalTrees*10
            time = str(time/60) + "hrs" if time/60 > 1 else str(time) + "min"
            text+='\nTotal time to make: '+time
            text+='\nOrder:'
            trees={x.split(":")[0]: x.split(":")[1] for x in contents.split('\n')[1:]}
            if len(trees) < totalTrees:
                text+="\nThis pattern is not possible to recreate\n-1"
            else:
                for y in range(int(contents.split("\n")[0])):
                    for x in range(int(contents.split("\n")[0])):
                        text+="\n"+trees[str(x)+","+str(int(contents.split("\n")[0])-1-y)]
            
            open("export.txt", "w").write(text)
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clearButton.collidepoint(pygame.mouse.get_pos()):
                clear()
        paint.processEvents(event)
    screen.fill((255, 255, 255))
    generator.updateScreen(screen, (800, 0))
    paint.updateScreen(screen, (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), clearButton)
    pygame.display.update()
    clock.tick(60)
