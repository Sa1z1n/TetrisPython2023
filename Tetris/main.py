import pygame
import pygame as pg
import random, time, sys
from pygame.locals import *
pygame.init()

fps = 25
window_w, window_h = 700, 800
clock = pygame.time.Clock()
block, cup_h, cup_w = 30, 30, 15
screen = pg.display.set_mode((window_w, window_h))

fon = pg.image.load("Images/Fon.jpg")


side_freq, down_freq = 0.15, 0.1
grid = []

side_margin = int((window_w - cup_w * block) / 60)
top_margin = window_h - (cup_h * block) - 5

colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30),
               (255, 255, 30))

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
brd_color, bg_color, txt_color, title_color, info_color = white, black, white, colors[2], colors[1]

fig_w, fig_h = 5, 5
empty = 'o'

figures = {'S': [['oooooo',
                  'oooooo',
                  'ooxxoo',
                  'oxxooo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'ooxxoo',
                  'oooxoo',
                  'oooooo']],
           'Z': [['oooooo',
                  'oooooo',
                  'oxxooo',
                  'ooxxoo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'oxxooo',
                  'oxoooo',
                  'oooooo']],
           'J': [['oooooo',
                  'oxoooo',
                  'oxxxoo',
                  'oooooo',
                  'oooooo'],
                 ['oooooo',
                  'ooxxoo',
                  'ooxooo',
                  'ooxooo',
                  'oooooo'],
                 ['oooooo',
                  'oooooo',
                  'oxxxoo',
                  'oooxoo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'ooxooo',
                  'oxxooo',
                  'oooooo']],
           'L': [['oooooo',
                  'oooxoo',
                  'oxxxoo',
                  'oooooo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'ooxooo',
                  'ooxxoo',
                  'oooooo'],
                 ['oooooo',
                  'oooooo',
                  'oxxxoo',
                  'oxoooo',
                  'oooooo'],
                 ['oooooo',
                  'oxxooo',
                  'ooxooo',
                  'ooxooo',
                  'oooooo']],
           'I': [['ooxooo',
                  'ooxooo',
                  'ooxooo',
                  'ooxooo',
                  'oooooo'],
                 ['oooooo',
                  'oooooo',
                  'xxxxoo',
                  'oooooo',
                  'oooooo']],
           'O': [['oooooo',
                  'oooooo',
                  'oxxooo',
                  'oxxooo',
                  'oooooo']],
           'T': [['oooooo',
                  'ooxooo',
                  'oxxxoo',
                  'oooooo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'ooxxoo',
                  'ooxooo',
                  'oooooo'],
                 ['oooooo',
                  'oooooo',
                  'oxxxoo',
                  'ooxooo',
                  'oooooo'],
                 ['oooooo',
                  'ooxooo',
                  'oxxooo',
                  'ooxooo',
                  'oooooo']]}


def pauseScreen():
    pause = pg.Surface((800, 935), pg.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (1, 1))

def runMusic():
    pygame.mixer.music.load("Sounds/Subway.mp3")
    pygame.mixer.music.play(-1)

def failMusic():
    pygame.mixer.music.load("Sounds/Fail.mp3")
    pygame.mixer.music.play(1)
def sound():
    pg.mixer.Sound("Sounds/delete.ogg")

def main():
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    display_surf.blit(fon, (0,0))
    basic_font = pg.font.SysFont('arial', 30)
    big_font = pg.font.SysFont('verdana', 50)
    pg.display.set_caption('Tetris')
    showText('Tetris')
    while True:
        runTetris()
        pauseScreen()
        showText('Game over')




def runTetris():
    global event
    cup = emptycup()
    runMusic()
    vol = 0.5
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()


    while True:



        if fallingFig == None:

            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()

            if not checkPos(cup, fallingFig):
                return failMusic()
        quitGame()
        for event in pg.event.get():
            if event.type == KEYUP:

                if event.key == K_SPACE:
                    pauseScreen()
                    pg.mixer.music.pause()
                    showText('Pause')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                    if event.key == K_SPACE:
                        pg.mixer.music.unpause()
                elif event.key == pg.K_1:
                    vol -= 0.1
                    pg.mixer.music.set_volume(vol)
                    print(pg.mixer.music.get_volume())
                elif event.key == pg.K_2:
                    vol += 0.1
                    pg.mixer.music.set_volume(vol)
                    print(pg.mixer.music.get_volume())
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

                clock.tick(fps)

            elif event.type == KEYDOWN:

                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()


                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])



                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()


                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1


        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:
            if not checkPos(cup, fallingFig, adjY=1):
                addToCup(cup, fallingFig)
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else:
                fallingFig['y'] += 1
                last_fall = time.time()


        display_surf.blit(fon, (0, 0))
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig != None:
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(fps)




def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stopGame():
    pg.quit()
    sys.exit()



def checkKeys():

    quitGame()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    display_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую кнопку, чтобы продолжить', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pg.display.update()
        fps_clock.tick()


def quitGame():
    for event in pg.event.get(QUIT):
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pg.event.post(event)


def calcSpeed(points):

    level = int(points / 5) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def getNewFig():

    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(cup_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


def addToCup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup():
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup


def incup(x, y):
    return x >= 0 and x < cup_w and y < cup_h


def checkPos(cup, fig, adjX=0, adjY=0):

    for x in range(fig_w):
        for y in range(fig_h):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def isCompleted(cup, y):

    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True


def clearCompleted(cup):

    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1

    return removed_lines


def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):

    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def gamecup(cup):


    pg.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8),
                 5)

    pg.draw.rect(display_surf, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))


    for a in range(cup_w):
        for b in range(cup_h):
            drawBlock(a, b, cup[a][b])



def volume():
    pg.mixer.music.get_volume()

def drawInfo(points, level):
    pointsSurf = basic_font.render(f'Баллы: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 200, 350)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 200, 400)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 200, 450)
    display_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_w - 200, 500)
    display_surf.blit(escbSurf, escbRect)

    infSurf = basic_font.render('↓ Громкости: 1 ', True, info_color)
    infRect = infSurf.get_rect()
    infRect.topleft = (window_w - 200, 550)
    display_surf.blit(infSurf, infRect)

    infSurf1 = basic_font.render('↑ Громкости: 2 ', True, info_color)
    infRect1 = infSurf1.get_rect()
    infRect1.topleft = (window_w - 200, 600)
    display_surf.blit(infSurf1, infRect1)

    infSurf2 = basic_font.render(volume(), True, info_color)
    infRect2 = infSurf1.get_rect()
    infRect2.topleft = (window_w - 200, 650)
    display_surf.blit(infSurf2, infRect2)


def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])


    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def drawnextFig(fig):
    nextSurf = basic_font.render('Следующая:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 200, 20)
    display_surf.blit(nextSurf, nextRect)
    drawFig(fig, pixelx=window_w - 200, pixely=100)


if __name__ == '__main__':
    main()