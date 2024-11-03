import pygame

def px_by_px(square:pygame.Rect, img:pygame.Surface):
    aver = 0
    pixel_count = square.width**2
    avg = [0, 0, 0]
    for x in range(square.width-1):
        for y in range(square.width-1):
            try:
                color = img.get_at((x+square.left, y+square.top))
            except IndexError:
                continue
            avg = [avg[i] + color[i] for i in range(len(avg))]
    return [i/pixel_count for i in avg]

def pixel(src:str,out:str , subdivisions=1):
    img = pygame.image.load(src)
    side = subdivisions
    outImg = pygame.Surface((side, side))
    squareSize = int(img.get_width()/subdivisions)
    for y in range(side):
        for x in range(side):
            square = pygame.Rect((x*squareSize, y*squareSize), (squareSize, squareSize))
            pygame.draw.rect(outImg, px_by_px(square, img), ((x, y), (1, 1)))
    pygame.image.save(outImg, out)
