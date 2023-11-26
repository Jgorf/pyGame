import pygame
from words import wordList, wordsOfLen
import random
pygame.init()

width = 1550
height = 800

#colors
green = '#538d4e'
yellow = '#b59f3b'
gray = '#3a3a3c'
kbGray = (129, 131, 132)
unfilledOutline = (58, 58, 60)
filledOutline = '#565758'
background = (18, 18, 19)

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen.fill(background)
pygame.display.set_caption("Wordle Clone")
clock = pygame.time.Clock()

#fonts
titleFont = pygame.font.Font('assets/fonts/titlefont.ttf', 40) 
lettersFont = pygame.font.Font('assets/fonts/letters.ttf', 32)
enterFont = pygame.font.Font('assets/fonts/letters.ttf', 20)
keyFont = pygame.font.Font('assets/fonts/letters.ttf', 25)
msgFont = pygame.font.Font('assets/fonts/letters.ttf', 18)

title_surf = titleFont.render("pyWordle", False, 'White')
title_rect = title_surf.get_rect(center = (screen.get_width() // 2 ,40))

keyList = ["QWERTYUIOP","ASDFGHJKL","ZXCVBNM"]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

global numLets
numLets = 0 #make menu to select amnt of letters


def createTiles(numLetters = 5):
	global hidden
	hidden = random.choice(wordsOfLen(wordList, numLetters))
	global tileWidth #also is tileHeight
	tileWidth = 62
	tileGap = 30
	totalTileWidth = (tileWidth + tileGap) * (numLetters - 1) + tileWidth
	xInitial = (screen.get_width() - totalTileWidth) // 2
	tile_x_pos = xInitial
	tile_y_pos = 150
	tileRects = [] #holds a list of rectangles which gives access to locations for the tiles
	for row in range(6):
		rowRects = []             
		for col in range(numLetters):
			rowRects.append(pygame.Rect)
		tileRects.append(rowRects)        
	
	for row in range(6):
		for col in range(numLetters):
			tile_surf = pygame.Surface((tileWidth, tileWidth))
			tile_surf.fill(background)
			tile_rect = tile_surf.get_rect(midleft = (tile_x_pos, tile_y_pos))
			tileRects[row][col] = (tile_rect)
			pygame.draw.rect(tile_surf, unfilledOutline, tile_surf.get_rect(), 2, 2) #params: (Surface, ColorValue, RectValue, width, border_radius)
			screen.blit(tile_surf,tile_rect)
			tile_x_pos += tileGap + tileWidth
		tile_x_pos = xInitial
		tile_y_pos += 83
	return tileRects

def addLetter(tileRect, letter, outlineColor = filledOutline, tileColor = None):
	outlineRect = pygame.Rect(tileRect.x, tileRect.y, tileWidth, tileWidth) #RectValue for outline rectangle
	innerRect = pygame.Rect(tileRect.x, tileRect.y, tileWidth - 2, tileWidth - 2) #RectValue for background of letter
	if tileColor: #if tile color exitst create colored background
		pygame.draw.rect(screen, tileColor, innerRect, 0, 2) #inside color (gray/green/yellow)
	pygame.draw.rect(screen, outlineColor, outlineRect, 2, 2) #outline (fill/unfilled)
	tileTxt_surf = lettersFont.render(letter, True, "White") 
	tileTxt_rect = tileTxt_surf.get_rect(center = (tileRect.x + tileWidth // 2, tileRect.y + tileWidth // 2))
	screen.blit(tileTxt_surf,tileTxt_rect)
	pygame.display.update()

def removeLet(tileRect): #need params
	innerRect = pygame.Rect(tileRect.x, tileRect.y, tileWidth - 2, tileWidth - 2)
	outlineRect = pygame.Rect(tileRect.x, tileRect.y, tileWidth, tileWidth)
	pygame.draw.rect(screen, background, innerRect, 0, 2)
	pygame.draw.rect(screen, unfilledOutline, outlineRect, 2, 2)
	pygame.display.update()

def count(word, letter):
	amnt = 0
	for let in word:
		if let == letter:
			amnt += 1
	return amnt

def createKb(keys):
	global kbWidth, kbHeight 
	kbWidth = 40
	kbHeight = 45
	kbGap = 10
	rowWidths = [(kbWidth + kbGap) * (len(keyRow) - 1) + kbWidth for keyRow in keys]
	rowWidths = sorted(rowWidths) #smallest keyRow width to largest
	maxRowWidth = max(rowWidths) #top keyRow
	xInitial = (screen.get_width() - maxRowWidth) // 2
	
	key_x_pos = xInitial
	key_y_pos = 620 #initially at 620px down from the top of the screen
	z_key_xPos = xInitial + 75
	m_key_xPos = z_key_xPos + rowWidths[0] 
	kbRects = [[pygame.Rect for col in range(len(keys[row]))] for row in range(3)] #holds the rectangles of the keys on the keyboard (access their positions)
	col = 0
	for rowInd in range(3):
		for key in keys[rowInd]: #loops through keys in the row of keys at the current row(0,1 2)
			keyBgRect = pygame.draw.rect(screen, kbGray, (key_x_pos, key_y_pos, kbWidth, kbHeight), 0, 4)
			key_surf = keyFont.render(key, True, "White")
			key_rect = key_surf.get_rect(center = (key_x_pos + kbWidth // 2 ,key_y_pos + kbHeight // 2))
			screen.blit(key_surf,key_rect)
			key_x_pos += (kbWidth + kbGap)
			kbRects[rowInd][col] = keyBgRect
			col += 1
		col = 0
		key_y_pos += (kbHeight + kbGap) #adds 10 pixels in between each row

		if rowInd == 0:
			key_x_pos = xInitial + 25
		if rowInd == 1:
			key_x_pos = xInitial + 75
	enterBgRect = pygame.Rect((z_key_xPos - 80, key_y_pos - 55), (70, kbHeight))
	enterSurf = enterFont.render("Enter", True, "white")
	enterRect = enterSurf.get_rect(center = (enterBgRect.x + 35, enterBgRect.y + kbHeight // 2))

	delBgRect = enterBgRect.copy()
	delBgRect.x = m_key_xPos + kbGap
	delSurf = pygame.image.load('assets/imgs/delKey.png')
	delRect = delSurf.get_rect(center = (delBgRect.x + 35, delBgRect.y + kbHeight // 2))
	pygame.draw.rect(screen, kbGray, enterBgRect, 0, 4)
	pygame.draw.rect(screen, kbGray, delBgRect, 0, 4)
	screen.blit(enterSurf, enterRect)
	screen.blit(delSurf, delRect)
	return kbRects
	

def updateKb(guessLet, bgColor = kbGray): #updates background color of guessed letter to inform user of what letters are in/not in word
	colInd = 0
	for rowInd in range(3):
		for key in keyList[rowInd]:  #keyList holds a list of each row of keys
			if key == guessLet:
				kbRect = kbPos[rowInd][colInd]
				pygame.draw.rect(screen, bgColor, (kbRect.x, kbRect.y, kbWidth, kbHeight), 0, 4)
				key_surf = keyFont.render(key, True, "White")
				key_rect = key_surf.get_rect(center = (kbRect.x + kbWidth // 2,kbRect.y + kbHeight // 2))
				screen.blit(key_surf,key_rect)
			colInd += 1
		colInd = 0
	pygame.display.update()

def toggleAlert(screen, message, show, start, duration):
	currTime = pygame.time.get_ticks()
	if show:
		msg_surf = msgFont.render(message, True, 'white')
		bg_pos = (title_rect.x - 65, title_rect.y - 5, 250, 55)
		msg_bg = pygame.draw.rect(screen,green, bg_pos, 0, 4)
		msg_rect = msg_surf.get_rect(center = (msg_bg.centerx, msg_bg.centery))
		screen.blit(msg_surf, msg_rect)

		if currTime >= start + duration:
			msg_surf = msgFont.render("", True, 'black')
			msg_bg = pygame.draw.rect(screen,background, bg_pos, 0, 4)
			screen.blit(title_surf,title_rect)
			pygame.draw.line(screen, '#3a3a3c', (0, 80) , (screen.get_width(), 80), 2)
			show = False
			if message != "Not in word list" and  message != "Not enough letters":
				pygame.quit()
				exit()
		
	pygame.display.update()
	return show

def checkGuess(guess: str, secret: str, currRow: int):
	secret = secret.upper()
	currGuess = "" #holds each letter that has been guessed so far
	global showingAlert, start_time, displayAlert, message, duration
	color = gray
	if guess.lower() not in wordList:
		displayAlert = True
		start_time = pygame.time.get_ticks()
		showingAlert = True
		message = "Not in word list"
	else: 
		displayAlert = False
		showingAlert = False
		duration = 2500
		for i in range(numLets): #i is the index that represents the current letter in the strings guess and secret as well as the current column in the tiles
			if guess[i] == secret[i]:
				color = green
			elif guess[i] in secret:
				#does not color a letter yellow if there is only one of that letter in the secret word and one or more than one of that letter in the inputted guess and if the current guess already contains a yellow/green version of that letter or if a green letter will occur later
				if count(secret, guess[i]) == 1 and count(guess, guess[i]) > 1 and (count(currGuess, guess[i]) >= 1 or guess.find(guess[i], i + 1) == secret.find(guess[i])):
					color = gray
				else:
					color = yellow
			else:
				color = gray
			addLetter(tilePos[currRow][i], guess[i], color, color)
			updateKb(guess[i], color)
			currGuess += guess[i]
		if currRow == 5 and guess != secret:
			start_time = pygame.time.get_ticks()
			displayAlert = True
			showingAlert = True
			message = f"The word was {secret}"
		elif guess == secret:
			start_time = pygame.time.get_ticks()
			displayAlert = True
			showingAlert = True
			message = "You Win!!"	
	return (guess.lower() in wordList) #returns True if in list False if not(used for determining to go to next guess or not)
		
def showSettings(isActive):
	btnTxt = ['4', '5', '6', '7', '8', '9']
	btnSize = 80
	btnGap = 30
	numLets = 0
	film = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
	film.fill((9, 9, 9, 80)) 
	menuWidth = 900
	menuHeight = 700
	centerPos = ((screen.get_width() - menuWidth) // 2, 82) #location of the third tile in first row inthe default 5 board game
	menu = pygame.draw.rect(screen, '#121213', (centerPos[0], centerPos[1], menuWidth, menuHeight), 0, 4)
	menuTxt = lettersFont.render("Select how many letters to play with:", True, 'white')
	menuRect = menuTxt.get_rect(center = (menu.centerx ,menu.top + 60))
	# draw the film over the screen
	screen.blit(film, (0, 0))
	screen.blit(menuTxt, menuRect)

	xInitial = menu.midleft[0] + menuWidth // 3
	yInitial = menu.top + menu.height // 2 - (btnSize + btnGap // 2)
	xPos = xInitial  
	yPos = yInitial
	
	tilePos, kbPos = [[]], [[]]
	for i in range(6):
		btnSurf = msgFont.render(btnTxt[i], True, 'white')
		btnBg = pygame.draw.rect(screen, kbGray, (xPos, yPos, btnSize + 2, btnSize + 2), 0, 4)
		btnRect = btnSurf.get_rect(center = (btnBg.centerx, btnBg.centery))
		screen.blit(btnSurf, btnRect)
		xPos += btnGap + btnSize
		if i == 2: #i is 3 when the fourth button is placed
			xPos = xInitial
			yPos += btnSize + btnGap

		if pygame.mouse.get_pressed()[0]: 
			if btnRect.collidepoint(pygame.mouse.get_pos()):#left clicked mouse and cursor is on button
				numLets = int(btnTxt[i])
				screen.fill(background)
				screen.blit(title_surf,title_rect)
				pygame.draw.line(screen, '#3a3a3c', (0, 80) , (screen.get_width(), 80), 2)
				tilePos = createTiles(numLets)
				kbPos = createKb(keyList)
				isActive = True
				break
			
			
	pygame.display.update()
	return numLets, tilePos, kbPos, isActive

global currCol, currRow
currRow = 0
currCol = 0
currGuess = ""
onLastLet = False
global kbPos, tilePos
kbPos, tilePos = [[]], [[]]
showingAlert = False
message = ""
displayAlert = False
game_active = False
duration = 1000
settingsMenu = (numLets, tilePos, kbPos, game_active)
start_time = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: #exit game
				pygame.quit()
				exit()
			if game_active and not showingAlert:
				letter = pygame.key.name(event.key).upper()
				if event.key == pygame.K_RETURN: #sends guess to be checked and moves to next row for new guess
					if onLastLet:
						isValidGuess = checkGuess(currGuess, hidden, currRow)
						if isValidGuess:
							#displayAlert = False
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
						removeLet(tilePos[currRow][currCol])
					if onLastLet: #set the onLastLet variable to false b/c after letter is removed your not on last letter anymore
						onLastLet = False
						
					currGuess = currGuess[0:currCol] #from first letter to the letter before currCol
					
				elif letter in alphabet: #is a letter in the alphabet
					if currRow < 6 and not onLastLet:
						addLetter(tilePos[currRow][currCol], letter)
						if currCol != numLets - 1: #keeps currCol index in range(highest currCol will be is the index of last let)
							currCol += 1
						currGuess += letter
					if len(currGuess) == numLets: #runs when current guess is 5th letters long
						onLastLet = True
	
		if event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			screen.fill(background)
			title_rect.center = (screen.get_width() // 2, 50)
			tilePos = createTiles()
			createKb(keyList)
	
	screen.blit(title_surf,title_rect)
	pygame.draw.line(screen, '#3a3a3c', (0, 80) , (screen.get_width(), 80), 2)

	
	numLets, tilePos, kbPos, game_active = settingsMenu
	if not game_active and numLets == 0:
		settingsMenu = showSettings(game_active)
		#isFirst = False
	if displayAlert:
		showingAlert = toggleAlert(screen, message, showingAlert, start_time, duration) #duration is in milliseconds (so 2000 is 2 seconds)

	pygame.display.update()
	clock.tick(60) #max framerate
