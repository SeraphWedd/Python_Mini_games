import pygame, sys, random, time
from pygame.locals import QUIT, MOUSEBUTTONUP, KEYUP, K_r

LENGTH = 600
WIDTH = 600

pygame.init()
WINSURF = pygame.display.set_mode((LENGTH,WIDTH))
pygame.display.set_caption("Tic Tac Toe!")

BFONT = pygame.font.SysFont('Arial', 24)
MFONT = pygame.font.SysFont('Arial', 60)

width = 100
length = 100

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
FPS = 24

CLOCK = pygame.time.Clock()


def drawboard():
    for x in range(1, 4):
        for y in range(1, 4):
            drawrect(x * 120, y * 120, white)
            

def drawmoves(moves_x, moves_o):
    for x in moves_x:
        if x in [1, 2, 3]:
            drawans(x*120, 120, "X")
        elif x in [4, 5, 6]:
            drawans((x-3)*120, 240, "X")
        elif x in [7, 8, 9]:
            drawans((x-6)*120, 360, "X")
            
    for o in moves_o:
        if o in [1, 2, 3]:
            drawans(o*120, 120, "O")
        elif o in [4, 5, 6]:
            drawans((o-3)*120, 240, "O")
        elif o in [7, 8, 9]:
            drawans((o-6)*120, 360, "O")


def drawans(top, left, token):
    if token == 'X':
        aSurf, aRect = makeTextObjs(token, MFONT, blue)
        aRect.center = (top + 50, left + 50)
        WINSURF.blit(aSurf, aRect)
    else:
        aSurf, aRect = makeTextObjs(token, MFONT, red)
        aRect.center = (top + 50, left + 50)
        WINSURF.blit(aSurf, aRect) 


def drawrect(top, left, col):
    pygame.draw.rect(WINSURF, col, (left, top, length, width))


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def checkwin(move):
    check = [False for x in range(9)]
    for i in move:
        check[i - 1] = True
    for ch in [[1,2,3], [4,5,6], [7,8,9], [1,4,7],
               [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:
        if (check[ch[0]-1] and check[ch[1]-1] and check[ch[2]-1]):
            return True
    else:
        return False

def top_flagger(text):
    topSurf, topRect = makeTextObjs(text, BFONT, white)
    topRect.center = (WIDTH/2, 50)
    WINSURF.blit(topSurf, topRect)

def bot_flagger(text):
    botSurf, botRect = makeTextObjs(text, BFONT, white)
    botRect.center = (WIDTH/2, 530)
    WINSURF.blit(botSurf, botRect)

    
def AI(mov_e, mov_ai):
    legal = [1, 9, 3, 7, 5, 2, 4, 6, 8]
    
    #Removes the already done move
    for a in mov_e + mov_ai:
        legal.remove(a)
        
    #Check if AI wins in next move
    for cmb in [[1,2,3], [4,5,6], [7,8,9], [1,4,7],
                    [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:    
        temp = 0
        mo = 0
        for i in cmb:
            if i in mov_ai:
                temp += 1
            else:
                mo = i
        if temp == 2:
            if mo in legal:
                return mo
        
    #Check if Enemy wins in next move
    for cmb in [[1,2,3], [4,5,6], [7,8,9], [1,4,7],
                    [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:    
        temp = 0
        mo = 0
        for i in cmb:
            if i in mov_e:
                temp += 1
            else:
                mo = i
        if temp == 2:
            if mo in legal:
                return mo

    #Check if the Enemy's first/last move is a corner
    if len(mov_e) > 0:
        if mov_e[-1] in [1, 3, 7, 9]:
            
            if 5 in legal:
                return 5
            
            elif 5 in mov_ai:
                if 2 in legal:
                    return 2
                elif 4 in legal:
                    return 4
                elif 6 in legal:
                    return 6
                elif 8 in legal:
                    return 8
        
        
    #Else move based on priority
    return legal[0]
        

def main():
    mov1 = []
    mov2 = []
    mov = random.randint(0, 1)
    game_won = False
    while True:
        WINSURF.fill(black)

        drawboard()
            
        if (len(mov1)!= 0 or len(mov2)!= 0):
            drawmoves(mov1, mov2)
        
        #AI MOVE
        if mov == 1 and not game_won:
            mov2.append(AI(mov1, mov2))
            mov = 0
        #END MOVE
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                px = mousex // 120
                py = mousey // 120
                loc = (py-1)*3 + px
                if loc not in mov1 and loc not in mov2:
                    if mov == 0 and not game_won:
                        mov1.append(loc)
                        mov = 1
                        
            elif event.type == KEYUP:
                if event.key == K_r and game_won:
                    mov1 = []
                    mov2 = []
                    game_won = False
                    mov = random.randint(0, 1)
                    
        if checkwin(mov1):
            top_flagger("Player wins!")
            game_won = True
            
        elif checkwin(mov2):
            top_flagger("Computer wins!")
            game_won = True
            
        elif len(mov1) + len(mov2) == 9:
            top_flagger("It's a DRAW!")
            game_won = True


        if game_won == False:
            bot_flagger(["Player's move", "Computer's move"][mov])
        else:
            bot_flagger("Press 'R' for Rematch!")
            
        pygame.display.update()
        CLOCK.tick(FPS)


if __name__=="__main__":
    main()
