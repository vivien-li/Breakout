import pygame

class Player(pygame.sprite.Sprite):
    """This class defines the sprite for the paddle/player"""
    def __init__(self, screen, player):
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define the image attributes for the paddle
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.player = player
        #Center the player horizontally in the window.
        self.rect.right = screen.get_width()/2 + 50
        #Determines the height based on player number
        if player == 1:
            self.rect.bottom = screen.get_height()
        else: 
            self.rect.top = 0
        self.window = screen
        self.dx = 0
    def changeDirection(self, xChange):
        self.dx = xChange
    def mouseDirection(self, position):
        """This method will cause the x direction to change based on the location of the mouse"""
        if self.rect.centerx > position:
            self.dx = -1
        elif self.rect.centerx < position:
            self.dx = 1
        self.position = int(position)
    def update(self):
        """This method is automatically called to reposition the player
        sprite on the screen."""
        #Check if we've moved to right/left of screen, if not keep moving
        if self.player == 1:
            if ((self.rect.right < self.window.get_width()) and self.dx > 0) or \
               ((self.rect.left > 0) and (self.dx < 0)): 
                self.rect.right += (self.dx*9)
        
        else:
            if self.dx == 1:
                if self.rect.centerx < self.position: 
                    if ((self.rect.right < self.window.get_width()) and self.dx > 0): 
                        self.rect.right += (self.dx*9)                     
            elif self.dx == -1:
                if self.rect.centerx > self.position:
                    if ((self.rect.left > 0) and (self.dx < 0)): 
                        self.rect.right += (self.dx*9)
              
class Ball(pygame.sprite.Sprite):
    """This class defines the sprite for the ball"""
    def __init__(self, screen, player):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # load appropriate image based on player number and set rect attributes for the Ball
        if player == 1:
            self.image = pygame.image.load("starbuckslogo.png")
            self.dy = 7
        else:
            self.image = pygame.image.load("ball2.png")
            self.dy = -7
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        #Position is determined based on player number and starting x direction
        if player == 1:
            self.rect.center = (screen.get_width()/2 + 5,screen.get_height()/4 * 3)
            self.dx = 6
        else:
            self.rect.center = (screen.get_width()/2 - 5, screen.get_height()/4)
            self.dx = -6    
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.window = screen

    def changeDirection(self):
        '''This method causes the y direction of the ball to reverse'''
        self.dy = -self.dy
        self.rect.left += self.dx
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        # Check if we have reached the left or the right of the screen
        # If not, then keep moving the ball in the same x direction. 
        if ((self.rect.left > 0) and (self.dx < 0)) or\
           ((self.rect.right < self.window.get_width()) and (self.dx > 0)):
            self.rect.left += self.dx
        # If yes, then reverse the x direction. 
        else:
            self.dx = -self.dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top > 0) and (self.dy > 0)) or\
           ((self.rect.bottom < self.window.get_height()) and (self.dy < 0)):
            self.rect.top -= self.dy
        # If yes, then reverse the y direction. 
        else:
            self.dy = -self.dy
            
class Brick(pygame.sprite.Sprite):
    '''The sprites for the brick.'''
    def __init__(self, screen, row, colourNum, xValue, yValue):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        colors = [(122, 199, 211), (133, 209, 89), (242, 145, 60), (252, 243, 111), (224, 87, 87), (206, 131, 219)]

        self.image = pygame.Surface([30, 15])
        self.image.fill(colors[colourNum])
        self.rect = self.image.get_rect()
        self.rect.centerx = xValue
        self.rect.centery = yValue
        self.points = row
    def getValue(self):
        """This method will return how much the brick is worth score wise"""
        return self.points
    
class ScoreKeeper(pygame.sprite.Sprite):
    """This class defines a label sprite to display the score"""
    def __init__(self, screen):
        "This initializer will load the custom font Santana-Bold and sets one variable to keep score for both players to zero and also set their combined health to 0"
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load font, set lives and score
        self.font = pygame.font.Font("Santana-Bold.ttf", 30)
        self.points = 0
        self.screen = screen
        self.lives = 3
    def addPoints(self, points):
        "This method will update the players score whenever it collides with a brick. Nothing\
        is returned"
        self.points += points 
    def setLives(self):
        "This mutator method will subtract one live from the players life"
        self.lives -= 1
    def getLives(self):
        "This method will return the current lives"
        return self.lives
    def gameOver(self):
        "This method will return 1 if all the bricks have been deleted (score of 432) or else return a 0"
        if self.points == 432:
            return 1
        else:
            return 0
    def update(self):
        message = "SCORE: " + str(self.points) + "     LIVES: " + str(self.lives)
        self.image = self.font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width()/2, 17)

class EndZone(pygame.sprite.Sprite):
    """This class defines the sprite for our endzones"""
    def __init__(self, screen, yPosition):
        '''This initializer takes a screen surface, and y position  as
        parameters.  For the bottom (player 1) endzone, yPosition will = screen height,
        and for the top (player 2) endzone, yPosition will = 1.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Our endzone sprite will be a 1 pixel wide black line.
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
                 
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.top = yPosition
        self.rect.left = 0        