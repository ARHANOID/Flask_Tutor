import pygame, sys, math
from pygame.locals import *

WINDOWWIDTH = 1024
WINDOWHEIGHT = 840
FPS = 1

center_width = WINDOWWIDTH // 2
center_height = WINDOWHEIGHT // 2
step = WINDOWHEIGHT // 6
zero = '0'
cross = 'X'
mass = [zero, cross]

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

Projectile_speed = 3

def game_start():
    DISPLAYSURF.fill(NAVYBLUE)

    pygame.draw.line(DISPLAYSURF, ORANGE, (center_width - int(step * 1.0), WINDOWHEIGHT / 1.8),
                     (center_width - int(step * 1.0), WINDOWHEIGHT / 2.2), 5)
    pygame.draw.line(DISPLAYSURF, ORANGE, (WINDOWWIDTH / 2.9, center_height + int(step * 0.34)),
                     (WINDOWWIDTH / 2.6, center_height + int(step * 0.34)), 5)

    pygame.draw.line(DISPLAYSURF, ORANGE, (center_width , WINDOWHEIGHT / 1.8),
                     (center_width , WINDOWHEIGHT / 2.2), 5)
    pygame.draw.line(DISPLAYSURF, ORANGE, (WINDOWWIDTH / 2.9 + int(step * 1.0), center_height + int(step * 0.34)),
                     (WINDOWWIDTH / 2.6+ int(step * 1.0), center_height + int(step * 0.34)), 5)

    pygame.draw.line(DISPLAYSURF, ORANGE, (center_width + int(step * 1.0), WINDOWHEIGHT / 1.8),
                     (center_width + int(step * 1.0), WINDOWHEIGHT / 2.2), 5)
    pygame.draw.line(DISPLAYSURF, ORANGE, (WINDOWWIDTH / 2.9+ int(step * 2.0), center_height + int(step * 0.34)),
                     (WINDOWWIDTH / 2.6+ int(step * 2.0), center_height + int(step * 0.34)), 5)



def drawItems(item, x, y):
    fontObj = pygame.font.Font('freesansbold.ttf', WINDOWWIDTH // 25)
    textSurfaceObj = fontObj.render(item, True, GREEN)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def explosion(x,y, power =30):
    # pygame.draw.rect(DISPLAYSURF, ORANGE, (x-power, y-power, power, power))
    pygame.draw.circle(DISPLAYSURF, YELLOW, (int(x), int(y)), power)


def drawscore(x):
    return


def no_one_win():
    fontObj = pygame.font.Font('freesansbold.ttf', WINDOWWIDTH // 20)
    item = 'No one have won the game'
    textSurfaceObj = fontObj.render(item, True, RED, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def getbox(x, y):
    c = [2, 2]
    a = WINDOWWIDTH // 3
    b = WINDOWHEIGHT // 3
    if x < a:
        c[0] = 0
    elif x < a * 2:
        c[0] = 1
    if y < b:
        c[1] = 0
    elif y < b * 2:
        c[1] = 1
    return c


def center_box(box):
    center = [0, 0]
    a = WINDOWWIDTH // 3
    b = WINDOWHEIGHT // 3
    center[0] = box[0] * a + a // 2
    center[1] = box[1] * b + b // 2
    return center[0], center[1]

def flight(amo):
    x, y, xx, yy = amo
    x1, x2= xx, xx
    y1, y2= yy, yy
    if abs(x - xx) > Projectile_speed:
        x1 = xx - Projectile_speed*math.copysign(1, x - xx)
        x2 = xx + Projectile_speed*math.copysign(1, x - xx)
    if abs(y - yy) > Projectile_speed:
        y1 = yy - Projectile_speed * math.copysign(1, y - yy)
        y2 = yy + Projectile_speed*math.copysign(1, y - yy)

    pygame.draw.circle(DISPLAYSURF, NAVYBLUE, (int(x1), int(y1)), 5)
    pygame.draw.circle(DISPLAYSURF, YELLOW, (int(x2), int(y2)), 3)








def gameWonAnimation(c):
    return

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    img1 = pygame.image.load("PH.jpg")
    pygame.display.set_icon(img1)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('PornHub')
    # pygame.display.set_icon(surface)
    # game_start()


    while True:
        # mouseClicked = False
        # first_clicl = True
        # drawscore(score)
        # Game_time += 1
        #
        # for i in range(len(amo_in_air)):
        #     boolcount = 0
        #     flight(amo_in_air[i])
        #     x, y, xx, yy = amo_in_air[i]
        #
        #     if abs(x - xx) < Projectile_speed:
        #         boolcount += 1
        #     else:
        #         xx += Projectile_speed*math.copysign(1, x - xx)
        #         print("xx", xx)
        #     if abs(y - yy) < Projectile_speed:
        #         boolcount += 1
        #     else:
        #         yy += Projectile_speed*math.copysign(1, y - yy)
        #         print("yy", yy)
        #     if boolcount == 2:
        #         explosion(x, y, 30)
        #         amo_in_air[i] = None
        #         print("explosion")
        #     else:
        #         amo_in_air[i] = (x, y, xx, yy)
        #         # amo_in_air.pop(elem)
        #         print("shot True", amo_in_air[i])
        #
        # if None in amo_in_air:
        #     amo_in_air.remove(None)
        # if None in amo_in_air:
        #     amo_in_air.remove(None)
        # if None in amo_in_air:
        #     amo_in_air.remove(None)
        # if None in amo_in_air:
        #     amo_in_air.remove(None)
        # if None in amo_in_air:
        #     amo_in_air.remove(None)
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # if Game_time % 30 == 0:
        #     drawItems(mass[counter % players], Game_time % 800, 60+40*(Game_time//800))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        #     elif event.type == MOUSEMOTION:
        #         mousex, mousey = event.pos
        #     elif event.type == MOUSEBUTTONUP:
        #         mousex, mousey = event.pos
        #         mouseClicked = True
        #
        # if mouseClicked:
        #
        #     a, b = center_box(getbox(mousex, mousey))
        #     print(a, b)
        #     expo = (mousex,mousey,center_height,center_width)
        #     amo_in_air.append(expo)
            # if game_state[getbox(mousex, mousey)[0]][getbox(mousex, mousey)[1]] == None:
            #     drawItems(mass[counter % players], a, b)
            #     counter += 1
            #     game_state[getbox(mousex, mousey)[0]][getbox(mousex, mousey)[1]] = (counter % players)
            #     a, b = check_winner(game_state)
            #     print('a,b', a, b)
            # print(game_state)

            # if a != None:
            #     score[a] += 1
            #     gameWonAnimation(b)
            #     game_state = [[None] * 3 for i in range(3)]
            #     counter = 0
            #
            # if game_end(game_state):
            #     pygame.display.update()
            #     pygame.time.wait(1000)
            #     no_one_win()
            #     pygame.display.update()
            #     pygame.time.wait(5000)
            #     game_start()
            #     counter = 0

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()