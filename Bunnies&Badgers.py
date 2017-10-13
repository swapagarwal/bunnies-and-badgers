# 0 loop_fix branch

 # 1 - Import library
import pygame
from pygame.locals import *
import math
import random
 
# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
pygame.mixer.init()
 
# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.set_volume(0.25)

 
# 4 - keep looping through
def main():
    keys = [False, False, False, False]
    playerpos=[100,100]
    acc=[0,0]
    arrows=[]
    badtimer=100
    badtimer1=0
    badguys=[[640,100]]
    healthvalue=194
    timestart = pygame.time.get_ticks()
    pygame.mixer.music.play(-1, 0.0)
    num_arrows = 100

    running = 1
    exitcode = 0
    while running:
        badtimer-=1
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - draw the screen elements
        for x in range(width/grass.get_width()+1):
            for y in range(height/grass.get_height()+1):
                screen.blit(grass,(x*100,y*100))
        screen.blit(castle,(0,30))
        screen.blit(castle,(0,135))
        screen.blit(castle,(0,240))
        screen.blit(castle,(0,345 ))
        # 6.1 - Set player position and rotation
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1)
        # 6.2 - Draw arrows
        for bullet in list(arrows):
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                arrows.remove(bullet)
                if num_arrows <= 0:
                    running = 0
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
        
       # 6.3 - Draw badgers
        if badtimer==0:
            badguys.append([640, random.randint(50,430)])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
        for badguy in list(badguys):
            if badguy[0]<-64:
                badguys.remove(badguy)
            badguy[0]-=7
            # 6.3.1 - Attack castle
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.remove(badguy)
            #6.3.2 - Check for collisions
            for bullet in list(arrows):
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    badguys.remove(badguy)
                    arrows.remove(bullet)
            # 6.3.3 - Next bad guy
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
        # 6.4 - Draw clock
        font = pygame.font.Font(None, 24)
        time_remaining = 90000 - (pygame.time.get_ticks() - timestart)
        survivedtext = font.render(str((time_remaining / 60000))+":"+str(time_remaining/1000%60).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[635,5]
        screen.blit(survivedtext, textRect)
        arrowstext = font.render("Remaining arrows: " + str(num_arrows), True, (0,0,0))
        arrowsTextRect = arrowstext.get_rect()
        arrowsTextRect.topright = [635, 20]
        screen.blit(arrowstext, arrowsTextRect)
        # 6.5 - Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button 
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit() 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position=pygame.mouse.get_pos()
                acc[1]+=1
                arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
                num_arrows -= 1
        # 9 - Move player
        if keys[0]:
            playerpos[1]-=5
        elif keys[2]:
            playerpos[1]+=5
        if keys[1]:
            playerpos[0]-=5
        elif keys[3]:
            playerpos[0]+=5
        #10 - Win/Lose check
        timenow = pygame.time.get_ticks()
        if timenow - timestart >=90000:
            running=0
            exitcode=1
        if healthvalue<=0:
            running=0
            exitcode=0
        if acc[1]!=0:
            accuracy=round(acc[0]*1.0/acc[1]*100,2)
        else:
            accuracy=0
    # 11 - Win/lose display        
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    elapsedtime = pygame.time.get_ticks()-timestart/1000

    game_over_message = ""
    if num_arrows <= 0:
        game_over_message = "You have run out of arrows!!! "
    game_over_message += "Score: "+str(accuracy)+"% (Accuracy) * "+str(elapsedtime/1000)+" (Time) = "+str(int(accuracy*elapsedtime/1000))
    text = font.render(game_over_message, True, (0, 255, 0))

    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    if exitcode==0:
        screen.blit(gameover, (0,0))
    else:
        screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
    pygame.display.flip()
    pygame.mixer.music.fadeout(1500)
    pygame.time.delay(1500)

    # draw replay/exit buttons
    global textx, texty, textx_size, texty_size
    global text2x, text2y, text2x_size, text2y_size
    bigfont = pygame.font.Font(None, 80)
    text = bigfont.render('Play Again', 13, (0, 255, 0))
    textx = width / 2 - text.get_width() / 2
    texty = height / 4 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(screen, (0, 255, 255), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))

    screen.blit(text, (width / 2 - text.get_width() / 2,
                       height / 4 - text.get_height() / 2))
    text2 = bigfont.render('Exit', 13, (255, 0, 0))
    text2x = width / 2 - text2.get_width() / 2
    text2y = height * 3 / 4 - text2.get_height() / 2
    text2x_size = text2.get_width()
    text2y_size = text2.get_height()
    pygame.draw.rect(screen, (0, 255, 255), ((text2x - 5, text2y - 5),
                                               (text2x_size + 10, text2y_size +
                                                10)))

    screen.blit(text2, (width / 2 - text2.get_width() / 2,
                       height * 3 / 4 - text2.get_height() / 2))


    pygame.display.flip()


main()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if x >= textx - 5 and x <= textx + textx_size + 5:
                if y >= texty - 5 and y <= texty + texty_size + 5:
                    main()
                    break
            if x >= text2x - 5 and x <= text2x + text2x_size + 5:
                if y >= text2y - 5 and y <= text2y + text2y_size + 5:
                    pygame.quit()
                    exit(0)
        
