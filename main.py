import random
import pygame
import math
import time
pygame.mixer.init()


mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()


pygame.mixer.music.load('sounds/forget.mp3')
pygame.mixer.music.play(-1)


# Set the screen size to be 18:9
screen_width = 400
screen_height = 800

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))


# Set the title and icon
pygame.display.set_caption("Space Wombo")
icon = pygame.image.load('img/ship.png')
pygame.display.set_icon(icon)

# Sparkling Dots for the background
class SparklingDot:
    def __init__(self, x, y, color, radius, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 0.5
        if self.lifetime <= 0:
            sparkling_dots.remove(self)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

sparkling_dots = []

def create_sparkling_dot():
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    color = (random.randint(200, 255), random.randint(200, 255), random.randint(0, 5))
    radius = random.randint(1, 2)
    lifetime = random.randint(100, 400)
    sparkling_dots.append(SparklingDot(x, y, color, radius, lifetime))


#SCORE
score = 0
money = pygame.mixer.Sound('sounds/mon.mp3')
# Increase the volume (e.g., 2.0 for a significant increase)
money.set_volume(0.5)
# Font and text settings
font = pygame.font.Font("assets/font.ttf", 22)
score_text = font.render(f"Score: {score}", True, (255, 255, 255))
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

#def get_font(size):
#    return pygame.font.Font("pygame tutorial notes/assets/font.ttf", size //1)



# Player's ship
playerImg = pygame.image.load('img/ship.png')
playerX = screen_width / 2 - playerImg.get_width() / 2
playerY = screen_height - playerImg.get_height()
playerX_change = 0
playerY_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

player_width = 64


#ENEMY
enemyX = screen_width / 2
enemyY = -100 
enemyY_change = 0.3
enemyX_change = 0.3
enemyImg = pygame.image.load('img/et.png')  # Load your enemy image
enemy_hit_img = pygame.image.load('img/et2.png') 
# Initialize enemy state
enemy_state = "normal"  # Start with the normal state


#BULLET
playerBullets = []

bullet = pygame.Rect(playerX + playerImg.get_width() / 2 - 2, playerY, 4, 10)  # Adjust the numbers for the bullet size and position


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:  # You can adjust this value based on your image size
        return True
    return False

shoot_sound = pygame.mixer.Sound('sounds/shot.mp3')
# Increase the volume (e.g., 2.0 for a significant increase)
shoot_sound.set_volume(2.5)

#PROPULSOR
def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return surf

# [loc, velocity, timer, color]
propulsors = []

# Asteroids
asteroidImgs = [pygame.image.load('img/ast1.png'),
                pygame.image.load('img/ast2.png'),
                pygame.image.load('img/ast3.png')]

asteroids = []

def create_asteroid():
    asteroidImg = random.choice(asteroidImgs)
    asteroidX = random.randint(0, screen_width - asteroidImg.get_width())
    asteroidY = random.randint(0, 100)
    asteroidX_change = 0
    asteroidY_change = random.uniform(0.1, 0.5)
    asteroids.append({"img": asteroidImg, "x": asteroidX, "y": asteroidY, "x_change": asteroidX_change, "y_change": asteroidY_change})

def draw_asteroid(asteroid):
    screen.blit(asteroid["img"], (asteroid["x"], asteroid["y"]))

running = True
asteroid_timer = 0  # Timer to control asteroid creation
asteroid_interval = 400  # Create a new asteroid every 100 frames

back = pygame.image.load("assets/background.png")
game_state = "playing"  # Puede ser "playing" o "game_over"



def game_over():
    global game_state
    game_state = "game_over"

    # Game Over screen
    while game_state == "game_over":
        screen.fill((0, 0, 0))  # Background
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2, screen_height / 2)
        screen.blit(text, text_rect)

        # Play Again button
        button_font = pygame.font.Font(None, 24)
        button_text = button_font.render("Play Again?", True, (255, 255, 255))
        button_rect = button_text.get_rect()
        button_rect.center = (screen_width / 2, screen_height / 2 + 50)
        screen.blit(button_text, button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Reset game variables and start a new game
                    game_state = "playing"
                    asteroids.clear()

        mainClock.tick(60)  # Limit frame rate

bullet = {
    'x': playerX + player_width / 2,
    'y': playerY,
    'speed': -5
}
playerBullets.append(bullet)


def start_game():
    global game_state, score
    game_state = "playing"
    score = 0



timeee = None  # Initialize the timeee variable outside the collision loop

def start_game():
    global game_state, score
    game_state = "playing"
    score = 0

game_state = "initial"

pygame.mixer.music.load('sounds/forget.mp3')
pygame.mixer.music.play(-1)


# Game LOOP
running = True
while running:
    if game_state == "initial":
        # Display the "Play" button
        play_button_image = pygame.image.load('img/play.png')
        button_rect = play_button_image.get_rect()
        button_rect.center = (screen_width // 2, screen_height // 2)
        screen.fill((1, 1, 45))
        screen.blit(play_button_image, button_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    start_game()  # Start the game when the button is clicked
    elif game_state == "playing":
            screen.fill((1, 1, 45))
            start_time = int (time.time())
            # Create new sparkling dots if there are fewer than 10
            if len(sparkling_dots) < 10:
                create_sparkling_dot()

            # Update and draw all sparkling dots
            for sparkling_dot in sparkling_dots:
                sparkling_dot.update()
                sparkling_dot.draw()

            # Adjust the values to create an ember-like effect
            propulsor_color = (255, random.randint(0, 150), 0)
            propulsor_radius = random.randint(2, 4)  # Smaller propulsors
            propulsors.append([[playerX + 32, playerY + 52], [random.uniform(-1, 1), random.uniform(1, 3)], random.randint(10, 20), propulsor_color])

            for propulsor in propulsors:
                propulsor[0][0] += propulsor[1][0]
                propulsor[0][1] += propulsor[1][1]
                propulsor[2] -= 1
                propulsor[1][1] += random.uniform(0.1, 0.2)

                if propulsor[2] <= 0:
                    propulsors.remove(propulsor)
                
                pygame.draw.circle(screen, propulsor[3], [int(propulsor[0][0]), int(propulsor[0][1])], propulsor_radius)


            # Update and draw all asteroids
            for asteroid in asteroids:
                asteroid["y"] += asteroid["y_change"]

                # Check for collision with player
                player_rect = pygame.Rect(playerX, playerY, playerImg.get_width(), playerImg.get_height())
                asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroid["img"].get_width(), asteroid["img"].get_height())
                if player_rect.colliderect(asteroid_rect):
                    score = 0
                    game_state = "game_over"  # End the game if the player collides with an asteroid
                    enemyY = -100
                    playerX = screen_width / 2 - playerImg.get_width() / 2
                    playerY = screen_height - playerImg.get_height()
                    playerX_change = 0
                    playerY_change = 0
                if asteroid["y"] > screen_height:
                    asteroids.remove(asteroid)
                else:
                    draw_asteroid(asteroid)

            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Set the key commands
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -1
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 1
                    if event.key == pygame.K_UP:
                        playerY_change = -1
                    if event.key == pygame.K_DOWN:
                        playerY_change = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -0.3
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 0.3
                    if event.key == pygame.K_UP:
                        playerY_change = -0.3
                    if event.key == pygame.K_DOWN:
                        playerY_change = 0.3
                    if event.key == pygame.K_SPACE:
                # Fire a bullet
                        shoot_sound.play()
                        bullet = {
                    'x': playerX + player_width / 2,
                    'y': playerY,
                    'speed': -5
                }
                    playerBullets.append(bullet)
                    # Play the shooting sound
                    
                    
            # Update enemy position (simplified horizontal movement)
            # Move the enemy
            if enemy_state == "normal":
        # Update enemy position only when not hit
                enemyX += enemyX_change
                enemyY += enemyY_change

            # Keep the enemy within the screen bounds
            if enemyX < 0:
                enemyX_change = 0.15
                enemyY += 20
            elif enemyX > screen_width - enemyImg.get_width():
                enemyX_change = -0.15
                enemyY += 20
            if enemyY < -100:
                enemyY = -100
            elif enemyY > screen_height - enemyImg.get_height():
                enemyY = screen_height - enemyImg.get_height()

            screen.blit(enemyImg, (enemyX, enemyY))

            # Update bullet positions
            for bullet in playerBullets:
                bullet['y'] += bullet['speed']
                pygame.draw.rect(screen, (255, 0, 0), (bullet['x'], bullet['y'], 2, 10))  # Bullet appearance

            # Enemy defeated logic

            # Create new asteroids at regular intervals
            asteroid_timer += 1
            if asteroid_timer >= asteroid_interval:
                create_asteroid()
                asteroid_timer = 0


            # Move the player
            playerX += playerX_change
            playerY += playerY_change

            # Keep the player within the screen bounds
            if playerX < -1:
                playerX = 400
            elif playerX >= 400:
                playerX = 0
            if playerY < 2:
                playerY = 2
            elif playerY > 740:
                playerY = 740
            
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, score_text_rect)

            for bullet in playerBullets:
                pygame.draw.rect(screen, (255, 0, 0), (bullet['x'], bullet['y'], 2, 10))  # Bullet appearance

            for bullet in playerBullets:
                bullet['y'] += bullet['speed']
                pygame.draw.rect(screen, (255, 0, 0), (bullet['x'], bullet['y'], 2, 10))  # Bullet appearance

                # Check for collisions with the enemy
                if is_collision(enemyX, enemyY, bullet['x'], bullet['y']):
                    playerBullets.remove(bullet)
                    if enemy_state == "normal":
                        money.play()
                        score += 1
                    # Change the enemy's state to "hit"
                        enemy_state = "hit"
                        enemyImg = pygame.image.load('img/et2.png')  # Change the enemy's image to the hit image
                        timeee = start_time
                if enemy_state == "hit":
                    if timeee is not None and timeee + 3 > start_time:
                            enemyX_change = 0
                            enemyY_change = 0
                    else:
                            enemy_state = "normal"
                            enemyImg = pygame.image.load('img/et.png')
                            enemyX = random.randint(0, screen_width - enemyImg.get_width())  # Reset the enemy position
                            enemyY = (random.randint(80,100)*-1)
                            enemyY_change = 0.3
                            enemyX_change = 0.3
            # Change the enemy's state back to "normal"
                    
                    

            # Draw the player, enemy, and bullets
            # Draw the player, enemy, and bullets
            player(playerX, playerY)

            # Update the display
            pygame.display.update()
            mainClock.tick(500)
            
            
            # Update the display
            pygame.display.update()
            x = 500
            y = x + (score*5)
            if y >= 1000:
                y = 1000
            mainClock.tick(x)
            print(y)


            

    elif game_state == "game_over":
        game_over()  # Handle the game over state

