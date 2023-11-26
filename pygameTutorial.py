import pygame
from random import randint
def display_scores():
	currTime = int((pygame.time.get_ticks() - startTime) / 1000)
	score_surf = scoreFont.render(str(currTime), False, (64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	score_bg_rect = (score_rect.x - 2, score_rect.y - 3, score_rect.width, score_rect.height)
	screen.blit(score_surf,score_rect)
	return currTime

def obstacle_movement(obstacles):
	if len(obstacles) > 0:
		for obstacle in obstacles:
			obstacle.x -= 5
			if obstacle.x < -100:
				obstacles.remove(obstacle)
			else:
				screen.blit(snail_surf,obstacle)
			print(obstacles)
	return obstacles

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
startTime = 0
#Game Title
scoreFont = pygame.font.Font('tutorialFiles/fonts/Pixeltype.ttf', 50) 
score = 0
gravity = 1 #constant acceleration downwards 


#background
sky_surf = pygame.image.load("tutorialFiles/graphics/Sky.png").convert_alpha() #makes it easier for pygame to work with images
ground_surf = pygame.image.load("tutorialFiles/graphics/ground.png").convert_alpha()
ground_rect = ground_surf.get_rect(topleft = (0,300))

#obstacles
snail_surf = pygame.image.load('tutorialFiles/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (randint(900, 1100), 300))

obstacle_rect_list = []

#player
player_surf = pygame.image.load('tutorialFiles/graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300)) #draws rectangele around surface (MAnipulate rectangle to manipulate character)
playerVelocity = 0

#Intro Screen
player_stand = pygame.image.load('tutorialFiles/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_title = scoreFont.render("Runner", False, (111,196,169))
game_title_rect = game_title.get_rect(center = (400, 80))

instructions_surf = scoreFont.render("Press space to run", False, (111,196,169))
instructions_rect = instructions_surf.get_rect(center = (400, 330))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

#states
game_active = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if not game_active:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game_active = True
					snail_rect.left = 800
					startTime = pygame.time.get_ticks()
		else:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
					playerVelocity = -20
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					playerVelocity = -20

		if event.type == obstacle_timer and game_active:
			obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))

	if game_active:
		#Environment
		screen.blit(sky_surf,(0,0))
		screen.blit(ground_surf,ground_rect)

		#score
		score = display_scores()




		obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		#player
		#print(player_rect.bottom)
		playerVelocity += gravity
		player_rect.bottom += playerVelocity
		
		if player_rect.bottom > 300: #under the floor or at the floor
			player_rect.bottom = 300
		
		screen.blit(player_surf, player_rect)

		#collisions
		for obstacle in obstacle_rect_list:
			if obstacle.colliderect(player_rect):
				game_active = False
				obstacle_rect_list = []

	else: #intro/menu screen
		screen.fill((94,129,162))
		screen.blit(player_stand, player_stand_rect)
		screen.blit(game_title, game_title_rect)
		score_message = scoreFont.render(f'Your score: {score}', False, (111,196,169))
		score_message_rect = score_message.get_rect(center = (400, 330))
		if score > 0:
			screen.blit(score_message, score_message_rect)
		else:
			screen.blit(instructions_surf, instructions_rect)
		
	pygame.display.update()
	clock.tick(60)



"""
Pygame Notes:

RECTANGLES:
	- To move a rectangle you can access the different points on a rectangle(top, left, right, bottom, centerx, centery) or use the rect_var.x or rect_var.y variable 

	Collisions:
		- player_rect.colliderect(snail_rect) returns 0(false) or 1(true)
			- since python automatically returns False for 0 in an if statement you dont need to check if player_rect.colliderect(snail_rect) == 1
			- just use if player_rect.colliderect(snail_rect):
			- Triggers multiple times which can be a problem such as when there is a health bar (YOu ay want some frames where u are invincible)
			- to make it only triger once you can do the following:

					if player_rect.colliderect(snail_rect):
						if not collided:
							collided = True
							print("collided")
					else:
						collided = False

		- rect1.collidepoint((x,y)) is another way to detect collisions with rectangles
			- checks if a point is inside a rectange 
			- returns 0(False) or 1(True) which can be used in an if statement
			- Used for mouse
	Drawing:
		draw using pygame.draw (Can be used to draw rectangles, circles, lines, points, ellipses, etc.)


Get mouse position:
	can be done in two ways
		1. pygame.mouse
			can give position or buttons being pressed
				- pygame.mouse.get_pos() -> returns a tuple holding the coordinates of the mouse
			
			can set visibility of mouse etc. 
		2. event loop to check events that check the mouse position
			- get MOUSEMOTION, clicks, position, etc. 
				- event.type == pygame.MOUSEMOTION


KEYBOARD INPUT:
	- MEthod 1: pygame.key
		- pygame.key.get_pressed() -> returns an object that holds all the states of the keys that can be clicked or are being clicked
		- usually you would store this in a variable like a dictionary
		- to access a certain key you can use indexing
			- keys[pygame.keyName] -> returns 0 or 1 which can be used in if statment

	- Method 2: event loop
		- check if event.type is equal to a type of keyboard input like (KEYDOWN, KEYUP, KEYMAPCHANGED)


Gives time since game started in milliseconds: pygame.time.get_ticks() 
	-time since we called pygame.init()
	- keeps going after game ended
	- 

TRANSFORM SURFACES: (scaling, rotating a surface and etc.)
	- transform methods 
	- 

TIMERS
	- we create a custom user event that is triggererd in certain time intervals
	- obstacle_timer = pygame.USEREVENT + 1
		- creates a new custom event
		- must add 1 to not conflict with other events defined by pygame. REFER to docs for more

	- pygame.time.set_timer(obstacle_timer, 900)	
		- triggers event in certain intervals
		- params: event and time in between triger in milliseconds
"""


