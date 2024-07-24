import pygame
from words import wordList, wordsOfLen
import random
import sys
pygame.init()

WIDTH = 1400
HEIGHT = 800

#colors
GREEN = '#538d4e'
YELLOW = '#b59f3b'
GRAY = '#3a3a3c'
KBGRAY = (129, 131, 132)
UNFILLEDOUTLINE = (58, 58, 60)
FILLEDOUTLINE = '#565758'
BACKGROUND = (18, 18, 19)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill(BACKGROUND)
pygame.display.set_caption("Wordle Clone")
CLOCK = pygame.time.Clock()

#fonts
titleFont = pygame.font.Font('assets/fonts/titlefont.ttf', 40) 
lettersFont = pygame.font.Font('assets/fonts/letters.ttf', 32)
enterFont = pygame.font.Font('assets/fonts/letters.ttf', 20)
keyFont = pygame.font.Font('assets/fonts/letters.ttf', 25)
msgFont = pygame.font.Font('assets/fonts/letters.ttf', 18)

title_surf = titleFont.render("pyWordle", False, 'White')
title_rect = title_surf.get_rect(center = (SCREEN.get_width() // 2 ,40))

keyList = ["QWERTYUIOP","ASDFGHJKL","ZXCVBNM"]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
keys = []

KBWIDTH = 40
KBHEIGHT = 45
KBGAP = 10

global numLets
numLets = 0 #make menu to select amnt of letters

#Represents the letter the user entered and that is drawn onto the tiles
class Letter:
    #initializes variables associated with Letter obj. (i.e. text displayed, tile rectangle for position, color)
	def __init__(self, text, tile_rect, tile_col = None, outline_col = FILLEDOUTLINE):
		self.text = text
		self.tile_rect = tile_rect
		self.tile_col = tile_col
		self.outline_col = outline_col

	#draws Letter object to screen
	def draw(self):
		outlineRect = pygame.Rect(self.tile_rect.x, self.tile_rect.y, tileWidth, tileWidth) #RectValue for outline rectangle
		innerRect = pygame.Rect(self.tile_rect.x, self.tile_rect.y, tileWidth - 2, tileWidth - 2) #RectValue for background of letter
		if self.tile_col: #if tile color exists, create colored background
			pygame.draw.rect(SCREEN, self.tile_col, innerRect, 0, 2) #inside color (gray/green/yellow)
		pygame.draw.rect(SCREEN, self.outline_col, outlineRect, 2, 2) #outline (fill/unfilled)
		tileTxt_surf = lettersFont.render(self.text, True, "White") 
		tileTxt_rect = tileTxt_surf.get_rect(center = (self.tile_rect.x + tileWidth // 2, self.tile_rect.y + tileWidth // 2))
		SCREEN.blit(tileTxt_surf,tileTxt_rect)
		pygame.display.update()

	#removes Letter object from tile
	def delete(self):
		#redraws an empty tile
		innerRect = pygame.Rect(self.tile_rect.x, self.tile_rect.y, tileWidth - 2, tileWidth - 2)
		outlineRect = pygame.Rect(self.tile_rect.x, self.tile_rect.y, tileWidth, tileWidth)
		pygame.draw.rect(SCREEN, BACKGROUND, innerRect, 0, 2)
		pygame.draw.rect(SCREEN, UNFILLEDOUTLINE, outlineRect, 2, 2)
		pygame.display.update()

#Class representing each key marked with the appropriate color to indicate the letters in/not in the word
class Key:
	#initializes variables associated with Key obj. (i.e. x & y position, letter displayed, background color for key, etc.)
	def __init__(self, x, y, letter):
		self.x = x
		self.y = y
		self.letter = letter
		self.color = KBGRAY
		self.rect = (x, y, KBWIDTH, KBHEIGHT) #rectangle used to draw background of each key with appropriate color

	#draws Key object to screen at correct (x,y) position with the letter instance variable
	def draw(self):
		pygame.draw.rect(SCREEN, self.color, self.rect, 0, 4)
		key_surf = keyFont.render(self.letter, True, "White")
		key_rect = key_surf.get_rect(center = (self.x + KBWIDTH // 2 ,self.y + KBHEIGHT // 2))
		SCREEN.blit(key_surf,key_rect)
		pygame.display.update()


def createKB():
	key_x, key_y = 455, 620

	for i in range(3):
		for letter in keyList[i]:
			key = Key(key_x, key_y, letter)
			keys.append(key)
			key.draw()
			key_x += (KBWIDTH + KBGAP)

		key_y += (KBHEIGHT + KBGAP)

		if i == 0:
			key_x = 480
		if i == 1:
			key_x = 530

def createTiles(numLetters=5):
    global hidden
    hidden = random.choice(wordsOfLen(wordList, numLetters))
    global tileWidth
    tileWidth = 62
    tileGap = 25
    totalTileWidth = (tileWidth + tileGap) * numLetters - tileGap
    xInitial = (SCREEN.get_width() - totalTileWidth) // 2
    tile_x_pos = xInitial
    tile_y_pos = 100
    tileRects = []  # holds a list of rectangles which gives access to locations for the tiles

    for row in range(6):
        rowRects = []
        for col in range(numLetters):
            tile_surf = pygame.Surface((tileWidth, tileWidth))
            tile_surf.fill(BACKGROUND)
            tile_rect = tile_surf.get_rect(topleft=(tile_x_pos, tile_y_pos))
            rowRects.append(Letter('', tile_rect))
            pygame.draw.rect(tile_surf, UNFILLEDOUTLINE, tile_surf.get_rect(), 2, 2)  # params: (Surface, ColorValue, RectValue, width, border_radius)
            SCREEN.blit(tile_surf, tile_rect)
            tile_x_pos += tileGap + tileWidth
        tile_x_pos = xInitial
        tile_y_pos += tileWidth + tileGap  # Assuming consistent gap between rows and columns
        tileRects.append(rowRects)

    return tileRects

#compares inputted guess with correct word
def checkGuess(guess: str, secret: str, currRow: int):
	secret = secret.upper()
	currGuess = "" #holds each letter that has been guessed so far
	global showingAlert, start_time, displayAlert, message, duration, game_result
	color = GRAY
	if guess.lower() not in wordList: #displays to the user the entered guess was not in word list
		displayAlert = True
		start_time = pygame.time.get_ticks()
		showingAlert = True
		message = "Not in word list"
	else: #colors Letters and Keys with appropriate colors based on guess
		displayAlert = False
		showingAlert = False
		duration = 2500
		for i in range(numLets):
			if guess[i] == secret[i]: #letter at the ith position equals letter in the ith position of secret word

				#sets new color to green for Letter object and for Key object with a letter equal to the ith letter of guess
				color = GREEN 
				for key in keys:
					if key.letter == guess[i]: 
						key.color = GREEN
						key.draw()

			elif guess[i] in secret:
				#doesn't color letter yellow if there is only one of that letter in the secret word and >= 1 of that 
				#letter in the inputted guess and if the current guess already contains a yellow/green version of that letter 
				#or if a green letter will occur later
				if count(secret, guess[i]) == 1 and count(guess, guess[i]) > 1 and (count(currGuess, guess[i]) >= 1 
							                                                   or guess.find(guess[i], i + 1) == secret.find(guess[i])):
					
					#sets new color to gray for Letter object and for Key object with a letter equal to the ith letter of guess
					color = GRAY
					for key in keys:
						if key.letter == guess[i]:
							key.color = GRAY
							key.draw()
				else:
					#sets new color to yellow for Letter object and for Key object with a letter equal to the ith letter of guess
					color = YELLOW
					for key in keys:
						if key.letter == guess[i]:
							key.color = YELLOW
							key.draw()
			else:
				#sets new color to gray for Letter object and for Key object with a letter equal to the ith letter of guess
				color = GRAY
				for key in keys:
						if key.letter == guess[i]:
							key.color = GRAY
							key.draw()
			
			#alters the color of the tile and outline for the Letter object at [currRow][i] and then redraws Letter
			letterPos[currRow][i].tile_col = color
			letterPos[currRow][i].outline_col = color
			letterPos[currRow][i].draw()
			pygame.display.update()

			currGuess += guess[i]

		if currRow == 5 and guess != secret: #Ran out of guesses and never got correct answer
			game_result = "L"

		elif guess == secret: #Correct answer found
			game_result = "W"
		
	return (guess.lower() in wordList) #returns True if in list False if not(used for determining to go to next guess or not)

def showSettings(isActive):
	btnTxt = ['4', '5', '6', '7', '8', '9']
	btnSize = 80
	btnGap = 30
	numLets = 0
	film = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
	film.fill((9, 9, 9, 80)) 
	menuWidth = 900
	menuHeight = 700
	centerPos = ((SCREEN.get_width() - menuWidth) // 2, 82) #location of the third tile in first row inthe default 5 board game
	menu = pygame.draw.rect(SCREEN, '#121213', (centerPos[0], centerPos[1], menuWidth, menuHeight), 0, 4)
	menuTxt = lettersFont.render("Select how many letters to play with:", True, 'white')
	menuRect = menuTxt.get_rect(center = (menu.centerx ,menu.top + 60))
	# draw the film over the screen
	SCREEN.blit(film, (0, 0))
	SCREEN.blit(menuTxt, menuRect)

	xInitial = menu.midleft[0] + menuWidth // 3
	yInitial = menu.top + menu.height // 2 - (btnSize + btnGap // 2)
	xPos = xInitial  
	yPos = yInitial
	
	letterPos = [[]]
	for i in range(6):
		btnSurf = msgFont.render(btnTxt[i], True, 'white')
		btnBg = pygame.draw.rect(SCREEN, KBGRAY, (xPos, yPos, btnSize + 2, btnSize + 2), 0, 4)
		btnRect = btnSurf.get_rect(center = (btnBg.centerx, btnBg.centery))
		SCREEN.blit(btnSurf, btnRect)
		xPos += btnGap + btnSize
		if i == 2: #i is 3 when the fourth button is placed
			xPos = xInitial
			yPos += btnSize + btnGap

		if pygame.mouse.get_pressed()[0]: 
			if btnRect.collidepoint(pygame.mouse.get_pos()):#left clicked mouse and cursor is on button
				numLets = int(btnTxt[i])
				SCREEN.fill(BACKGROUND)
				SCREEN.blit(title_surf,title_rect)
				pygame.draw.line(SCREEN, '#3a3a3c', (0, 80) , (SCREEN.get_width(), 80), 2)
				letterPos = createTiles(numLets)
				createKB()
				isActive = True
				break
			
			
	pygame.display.update()
	return numLets, letterPos, isActive

def count(word, letter):
	amnt = 0
	for let in word:
		if let == letter:
			amnt += 1
	return amnt

def toggleAlert(screen, message, show, start, duration):
	currTime = pygame.time.get_ticks()
	if show:
		msg_surf = msgFont.render(message, True, 'white')
		bg_pos = (title_rect.x - 65, title_rect.y - 5, 250, 55)
		msg_bg = pygame.draw.rect(screen, GREEN, bg_pos, 0, 4)
		msg_rect = msg_surf.get_rect(center = (msg_bg.centerx, msg_bg.centery))
		screen.blit(msg_surf, msg_rect)

		if currTime >= start + duration:
			msg_surf = msgFont.render("", True, 'black')
			msg_bg = pygame.draw.rect(screen, BACKGROUND, bg_pos, 0, 4)
			screen.blit(title_surf,title_rect)
			pygame.draw.line(screen, '#3a3a3c', (0, 80) , (screen.get_width(), 80), 2)
			show = False
			if message != "Not in word list" and  message != "Not enough letters":
				pygame.quit()
				sys.exit()
		
	pygame.display.update()
	return show

def replay():
	pygame.draw.rect(SCREEN, GRAY, (WIDTH // 2 - 300, 620, 600, 170))
	replay_surf = lettersFont.render("Press Enter to Play Again", True, 'White')
	replay_rect = replay_surf.get_rect(center=(WIDTH // 2, 730))

	correct_word_surf = lettersFont.render(f"The correct word was {hidden}", True, 'White')
	correct_word_rect = correct_word_surf.get_rect(center=(WIDTH // 2, 680))

	SCREEN.blit(correct_word_surf, correct_word_rect)
	SCREEN.blit(replay_surf, replay_rect)
	pygame.display.update()


def reset():
	global currCol, currRow, game_result, currGuess, onLastLet, showingAlert
	global message, displayAlert, duration, settingsMenu, start_time, letterPos
	currRow = 0
	currCol = 0
	currGuess = ""
	onLastLet = False
	letterPos = [[]]
	showingAlert = False
	message = ""
	displayAlert = False
	game_active = False
	duration = 1000
	start_time = 0
	game_result = ""
	settingsMenu = showSettings(game_active)


global currCol, currRow
currRow = 0
currCol = 0
currGuess = ""
onLastLet = False
letterPos = [[]]
showingAlert = False
message = ""
displayAlert = False
game_active = False
duration = 1000
settingsMenu = (numLets, letterPos, game_active)
start_time = 0
game_result = ""

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: #exit game
				pygame.quit()
				sys.exit()
			if game_active and not showingAlert:
				letter = pygame.key.name(event.key).upper()
				if event.key == pygame.K_RETURN: #sends guess to be checked and moves to next row for new guess
					if game_result:
						reset()
					elif onLastLet:
						isValidGuess = checkGuess(currGuess, hidden, currRow)
						if isValidGuess:
							currGuess = ""
							currRow += 1
							currCol = 0
							onLastLet = False
					else: #guess is shorter than the number of letters being played with
						showingAlert = True
						start_time = pygame.time.get_ticks()
						displayAlert = True
						message = "Not enough letters"

				elif event.key == pygame.K_BACKSPACE:
					if currCol > 0:
						if not onLastLet: #does not subtract one from currCol if on lastLetter so it actually removes last letter
							currCol -= 1 #removes one from currCol so the proper letter(one before letter at current col) is removed
						letterPos[currRow][currCol].delete()
					if onLastLet: #set the onLastLet variable to false b/c after letter is removed your not on last letter anymore
						onLastLet = False
						
					currGuess = currGuess[0:currCol] #from first letter to the letter before currCol
					
				elif letter in alphabet: #is a letter in the alphabet
					if currRow < 6 and not onLastLet:
						let = letterPos[currRow][currCol]
						let.text = letter
						let.draw()
						if currCol != numLets - 1: #keeps currCol index in range(highest currCol will be is the index of last let)
							currCol += 1
						currGuess += letter
					if len(currGuess) == numLets: #runs when current guess is 5th letters long
						onLastLet = True
	
	if game_result:
		replay()

	SCREEN.blit(title_surf,title_rect)
	pygame.draw.line(SCREEN, '#3a3a3c', (0, 80) , (SCREEN.get_width(), 80), 2)

	
	numLets, letterPos, game_active = settingsMenu
	if not game_active and numLets == 0:
		settingsMenu = showSettings(game_active)
		#isFirst = False

	if displayAlert:
		showingAlert = toggleAlert(SCREEN, message, showingAlert, start_time, duration) #duration is in milliseconds (so 2000 is 2 seconds)

	pygame.display.update()
	CLOCK.tick(60) #max framerate