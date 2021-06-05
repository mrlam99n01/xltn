import pygame
import os
import random
import numpy as np
from abc import ABC, abstractmethod
from spriteSheet import Spritesheet
from nameEntity import *
import math
import socket
x = 89
y = 22
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
#----------------------
class Entity:
	def __init__(self,posX,posY,screen,img):
		self.posX = posX
		self.posY = posY
		self.screen = screen
		self.image = pygame.image.load(os.path.join(os.getcwd() , "assets" ,img))
	
	@abstractmethod
	def draw(self,playerX_change,playerY_change):
		pass


#Player
class Player(Entity):
	def __init__(self,posX,posY,screen,img):
		super().__init__(posX,posY,screen,img)
		self.current_heath = 400
		self.maximum_heath = 1000
		self.heath_bar_length = 400
		self.heath_ratio = self.maximum_heath/self.heath_bar_length


	def draw(self,playerX_change,playerY_change,enemies):
		self.posX = self.posX + playerX_change
		self.collide(enemies)
		if self.posX < 0:
			self.posX = 0
		elif self.posX > 736:
			self.posX = 736
		self.screen.blit(self.image,(self.posX,self.posY))
		pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.heath_bar_length,25),4)
		pygame.draw.rect(self.screen, (255,0,0), (10,10,self.current_heath,25))


	def collide(self,enemies):	
		for enemy in enemies:
			if math.sqrt(pow(self.posX - enemy.posX,2) + pow(self.posY -enemy.posY,2)) < 40:
				print("collide")
				self.get_damage(50)
				enemy.posX = random.randint(0, 736)
				enemy.posY = random.randint(0, 120)



	def get_damage(self,amount):
		if self.current_heath > 0:
			self.current_heath -= amount
		if self.current_heath <= 0:
			self.current_heath = 0

	def get_heath(self,amount):
		if self.current_heath < self.maximum_heath:
			self.current_heath += amount
		if self.current_heath >= self.maximum_heath:
			self.current_heath = self.maximum_heath

	def get_current_heath(self):
		return  self.current_heath
		

#Asteroid
class Enemy(Entity):
	def __init__(self,posX,posY,screen,img):
		super().__init__(posX,posY,screen,img)

	def draw(self,playerX_change,playerY_change):
		self.posY = self.posY + playerY_change
		if self.posY > 600:
			self.posY = random.randint(0,120)  
			self.posX = random.randint(0,900)
		self.screen.blit(self.image,(self.posX,self.posY))	
#Bullet
class Bullet(Entity):
	def __init__(self,posX,posY,screen,img,state):
		super().__init__(posX,posY,screen,img)
		self.state = state

	def draw(self,playerX_change,playerY_change,enemies):
		if self.state == "FIRE":
			self.posY = self.posY + playerY_change
			self.collide(enemies)
			if self.posY <= 0:
				self.state = "READY"
			self.screen.blit(self.image,(self.posX,self.posY))	
	def collide(self,enemies):
		global  score_value
		for enemy in enemies:
			if math.sqrt(pow(self.posX - enemy.posX,2) + pow(self.posY -enemy.posY,2)) < 27:
				self.state = "READY"
				score_value +=1
				enemy.posX = random.randint(0,736) 
				enemy.posY = random.randint(0,120) 

		

#-----------------------------------------
## Main function




#screen, play, enemies, bullet 
screen = pygame.display.set_mode((800,600))
spaceShip = Player(370,480,screen,"spaceship.png")
spritesheet = Spritesheet("spaceship_sprite.png")



listOfAsteroid = [] 
for _ in range(0,3):
	listOfAsteroid.append(Enemy(random.randint(0,736),random.randint(0,80),screen,"asteroid.png"))
listOfBullet = np.array([])

#atrributes
playerX_change = 0
playerY_change = 0

#score
score_value = 0
print(pygame.font.get_fonts())
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
gameOverFont = pygame.font.SysFont('Comic Sans MS', 50)

#title and icon clock, background
pygame.display.set_caption("Space shooting")
icon  = pygame.image.load(os.getcwd()+"/alien.png") 
background  = pygame.image.load(os.getcwd()+"/background.jpg") 
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

#game loop
running = True

#buffer
buffer = []

while running:
	clock.tick(60)
	#RGB image
	screen.fill((0,0,0))
	#background image
	screen.blit(background,(0,0))
	score = font.render("Score "+str(score_value),True, (255,255,0))

	#screen.blit(spaceship_straight,(0,0))
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -1
				#spaceShip.draw(playerX_change,playerY_change,listOfAsteroid)
			if event.key == pygame.K_RIGHT:
				playerX_change = 1
				#spaceShip.draw(playerX_change,playerY_change,listOfAsteroid)
			if event.key == pygame.K_UP:
				for i in range(0,5):
					print("bullet")
					#bullet = Bullet(spaceShip.posX+16,spaceShip.posY+16,screen,"bullet.png","FIRE")
					listOfBullet = np.append(listOfBullet,Bullet(spaceShip.posX+37-i*10,spaceShip.posY+16,screen,"bullet.png","FIRE"))
				

		# if event.type == pygame.KEYUP:
		# 	if event.key == pygame.K_LEFT  or event.key == pygame.K_RIGHT:
		# 		playerX_change = 0
	#movement of entity	
	spaceShip.draw(playerX_change,playerY_change,listOfAsteroid)
	if spaceShip.get_current_heath() > 0:
		[asteroid.draw(0,1) for asteroid in listOfAsteroid]
		listOfNeededDestroyBullet = []
		for index in range(0,len(listOfBullet)):
			if listOfBullet[index].state == "READY":
				listOfNeededDestroyBullet.append(index)
			else:
				listOfBullet[index].draw(0,-3,listOfAsteroid)
		listOfBullet = np.delete(listOfBullet,listOfNeededDestroyBullet)
		screen.blit(score, (15, 30))
		pygame.display.update()
	else:
		spaceShip.draw(0,0,listOfAsteroid)
		gameOverText = gameOverFont.render("GAME OVER", True, (255, 255, 255))
		screen.blit(gameOverText, (300, 200))
		screen.blit(score, (300, 300))
		pygame.display.update()

	
