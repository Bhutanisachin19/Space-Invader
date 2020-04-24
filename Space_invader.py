
#space invader game using pygame

import pygame
import random
import math
from pygame import mixer # to handel music


#inialize the pygame
pygame.init()


#creating window
screen = pygame.display.set_mode((800,600)) #width and height

#background
background = pygame.image.load("space_background.png")


#background sound
mixer.music.load("background_music_cropped.wav")
#mixer.music.play() # if we eave () it will play once
# music for lage file , sound for small files like bullet 
mixer.music.play(-1)



#title and icon
pygame.display.set_caption("Space Invaders ")
icon = pygame.image.load("spaceship.png" )
pygame.display.set_icon(icon)

#player image and icon are same but size if different in my code

#Player
player_img = pygame.image.load("Player.png")
#coordinates depends on the screen size and the position of the player
playerX = 370
playerY = 480
playerX_change = 0


def player(x,y):
    screen.blit(player_img , (x , y))


#score display on screen
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10 
textY = 10
 

def show_score(x , y):
    # we use render because we display score
    score = font.render("Score : "+ str(score_value), True , (255,255,255))
    screen.blit(score, (x , y))


#game over text
over_font = pygame.font.Font("freesansbold.ttf",64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True , (255,255,255))
    screen.blit(over_text, (200, 250)) #middle of the screen
    

def game_over_sound():
    game_over_m = mixer.Sound("game_over_sound.wav")
    game_over_m.play()


 

#multiple enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):    
    enemy_img.append(pygame.image.load("enemy.png"))
    #coordinates depends on the screen size and the position of the player
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40) #to move down


def enemy(x , y, i ):
    screen.blit(enemy_img[i] , (x , y))


#bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480 #as player is at 480
bulletX_change = 0
bulletY_change = 4 #speed of bullet
#ready  means you cant see bullet on screen and fire means its moving or fired
bullet_state = "ready"



def fire_bullet(x,y):
    global bullet_state
    bullet_state= "fire"
    screen.blit(bullet_img , (x + 16 , y + 10)) # x + any y + so bullet appears in the center of spaceship



#collision
def isCollision(enemyX , enemyY , bulletX , bulletY):
    #formula -> distance between two coordinates
    #distance btwn bullet and enemy
    distance  = math.sqrt((math.pow(enemyX - bulletX,2)) +(math.pow(enemyY - bulletY,2)))

    if distance < 27 :
        #collision occured
        return True
    else:
        return False




#to hold the screen
running = True

while running:
    # R G B  (0 to 255)
    screen.fill((0 , 0 , 0)) #black

    #background image
    screen.blit(background , (0,0)) #0 ,0 to appear from the start
    # when we add background and it has to be loaded everytime so speed can be slow

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #cross button
            running= False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            #print("A key is pressed")
            if event.key == pygame.K_LEFT:
                #print("Left arrow pressed")
                playerX_change = -2
        
            if event.key == pygame.K_RIGHT:
                #print("Right arrow pressed")
                playerX_change = 2 

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("shot.wav")
                    bullet_sound.play()
                    #shoot bullet if space is pressed
                    #get current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX , bulletY)

        #release pressed key = keyup
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("Key Released")
                playerX_change = 0 #spaceship stops moving

    
    playerX += playerX_change #adding new coorinates

    #setting boundaries
    # using x because it is moving left and right i.e X 
    # Y is up and down
    if playerX <=0:
        playerX=0
    elif playerX >=736:
        #size of player img = 64*64 pixels so we subtract 64 from 800
        playerX = 736


    #for enemy
    # movement in x -> if enemy hits the boundary i.e 736 it should change the direction and move to left
    # movement in y -> if enemy hit boundary it should come down
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:#enemy come close to this coordinate
            for j in range(num_of_enemies):#all emenies are moved out of the scree i.e 2000
                enemyY[j] = 2000 #below the screen
            
            game_over_sound()
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i] ,enemyY[i] ,bulletX ,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1 
            #print(score_value)
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i] ,enemyY[i] , i)


    #bullet movement
    if bulletY <=0 :#when it goes outside the screen
        #to shoot more than one bullet
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY) #without this bullet wont appear on the screen
        bulletY -= bulletY_change

 
    player(playerX,playerY) #after screen fill  because screen is drawn first
    show_score(textX , textY) # to display score
    pygame.display.update() #to keep screen updated
 
 

