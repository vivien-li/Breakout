"""
NAME: VIVIEN LI
DATE: APRIL 26 2019
DESCRIPTION: WELCOME TO BREAKOUT v2.0! This new update is the Super-Duper Breakout 
version, which means the game is now two players with two balls. Double the fun!
The scoring has also changed, starting from the top to the bottom, the bricks 
are now scored 2, 4, 6, 6, 4, 2, but the colours still remain the same because
this game is JUST as fun!
"""
# I - IMPORT AND INTIALIZE
import pygame, breakoutSprites
pygame.init()
pygame.mixer.init()

def main():
    """This function defines the 'mainline logic' for my breakout game"""
    
    #D - DISPLAY
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Breakout! v1.0")
    
    #E - ENTITIES
    background = pygame.image.load("background.jpg")
    background = background.convert()
    screen.blit(background, (0, 0))
    
    #Sprites for player, ball, bricks, scorekeeper, endzone
    player1 = breakoutSprites.Player(screen, 1)
    player2 = breakoutSprites.Player(screen, 2)
    ball1 = breakoutSprites.Ball(screen, 1)
    ball2 = breakoutSprites.Ball(screen, 2)
    
    bricks = []
    xPosition = 56
    yPosition = 190
    rowTracker = 0
    pointsList = [2, 4, 6, 6, 4, 2]
    for row in range(5, -1, -1):
        for col in range(18):
            bricks.append(breakoutSprites.Brick(screen, pointsList[rowTracker], row, xPosition + col * 31, yPosition + (rowTracker) * 15))
        rowTracker += 1
    
    score = breakoutSprites.ScoreKeeper(screen)
    endZone1 = breakoutSprites.EndZone(screen, screen.get_height())
    endZone2 = breakoutSprites.EndZone(screen, 1)
    brickGroup = pygame.sprite.OrderedUpdates(bricks)
    allSprites = pygame.sprite.OrderedUpdates(bricks, ball1, ball2, player1, player2, score, endZone1, endZone2)
    
    #Game Over image and winner image to display once game loop is terminated
    gameOver = pygame.image.load("gameover.png")
    gameOver.convert()
    winner =pygame.image.load("winner.png")
    winner.convert()
    #MUSIC
    pygame.mixer.music.load("jingle.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    slurp = pygame.mixer.Sound("slurp.ogg")
    slurp.set_volume(0.2)
    
    punch = pygame.mixer.Sound("punch.wav")
    punch.set_volume(0.2)
    
    oof = pygame.mixer.Sound("oof.ogg")
    oof.set_volume(1)
    #ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    
    # L - LOOP
    while keepGoing:
        
        #TIME
        clock.tick(30)
        
        #E- EVENT HANDLING: Player users keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.changeDirection (-1)
                elif event.key == pygame.K_RIGHT:
                    player1.changeDirection(1)
            elif event.type == pygame.KEYUP:
                player1.changeDirection(0)
            elif event.type == pygame.MOUSEMOTION:
                player2.mouseDirection((pygame.mouse.get_pos()[0]))						
                
        #BALL AND PLAYER COLLISIONS            
        # Check if ball1 hits Player 1
        if ball1.rect.colliderect(player1.rect):
            ball1.changeDirection()
            ball1.rect.bottom = screen.get_height() - 16
            slurp.play()
        #Check if ball2 hits Player 1     
        if ball2.rect.colliderect(player1.rect):
            ball2.changeDirection()
            ball2.rect.bottom = screen.get_height() - 16
            slurp.play()
       #Check if ball 1 hits Player 2
        if ball1.rect.colliderect(player2.rect):
            ball1.changeDirection()
            ball1.rect.top = 16
            slurp.play()
        #Check if ball 2 hits Player 2
        if ball2.rect.colliderect(player2.rect):
            ball2.changeDirection()
            ball2.rect.top = 16 
            slurp.play()            
        #BRICK AND BALL COLLISION    
        # Check if ball1 hits the brick
        collision1 = pygame.sprite.spritecollide(ball1, brickGroup, False)
        if collision1:
            for brick in collision1:
                score.addPoints(brick.getValue())
                brick.kill()
            ball1.changeDirection()
            punch.play()
        # Check if ball2 hits the brick

        collision2 = pygame.sprite.spritecollide(ball2, brickGroup, False)
        if collision2:
            for brick in collision2:
                score.addPoints(brick.getValue())
                brick.kill()
            ball2.changeDirection()    
            punch.play()
 
        #BALL AND ENDZONE COLLISION
        # Check if they lose a life (i.e., ball1 hits player 1 endzone or player 2 endzone)
        if ball1.rect.colliderect(endZone1) or ball1.rect.colliderect(endZone2):
            score.setLives()
            ball1.changeDirection()
            oof.play()
            
        # Check if they lose a life (i.e., ball2 hits player 1 endzone or player 2 endzone)      
        if ball2.rect.colliderect(endZone1) or ball2.rect.colliderect(endZone2):
            score.setLives()
            ball2.changeDirection()     
            oof.play()
            
        #CHECK IF ALL BRICKS GONE OR NO MORE LIVES    
        if score.gameOver() == 1 or score.getLives() == 0:
            pygame.mixer.music.fadeout(2000)
            keepGoing = False
            
        #R - REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    #Display game over if lost
    if score.getLives() == 0:
        screen.blit(gameOver, (0, 0))
    elif score.gameOver() == 1:
        screen.blit(winner, (0, 0))
    pygame.display.flip()
    
    #Close the game window
    pygame.time.delay(2000)
    pygame.quit()

#Call the main function
main()