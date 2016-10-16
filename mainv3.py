################################
#The snake game implementation #
#Author: Rashmi Jasinghe       #
#Date started:10/14/2016       #
#Version : 1                   #
################################


#Features in working version 
#Game is functioning as it is supposed to
#Getting coin will increase the lenght of the snake 

#Features to add 
#Increase the speed of the snake
#More levels (use a textfile to sore level information)
#More coins
#A tutorials for new players 
#A menu

#Possible features 
#AI to compete against 
#Make it multiplayer (requires rewriting of the game engine as current one only accomodates 1 player)

"""IMPORTANT FIXES"""
"""
Need to make the constructor for snake segment and coin segment take in x and y arguments 
Need to use a tuple for the keys 
Need to use the next future position of the head to check for crash or if coin is caught 
"""

from random import randint
from SimpleGraphics import *
from time import sleep 

#fix coin
HEAD_INDEX = 0 	
MAXX = 50 #Max x coordinate of playing field 
MAXY = 50 #Max y coordinate of playing field 	
MINX = 0 #Min x coodinate of the playing field
MINY = 0 #Min y coordinate of the playing field	
ZOOM = 10 #Zoom factor 
HEIGHT = 10 #Height of an individual snake segment
WIDTH = 10 #Width of an individual snake segment

#container for holding the information of the coin
class Coin:
	def __init__(self):
		self.pos_x = randint(MINX+10,MAXX-2)
		self.pos_y = randint(MINY+10,MAXX-2)
		
	def update_coin (self):
		self.pos_x = randint(MINX+10,MAXX-2)
		self.pos_y = randint(MINY+10,MAXY-2)
	
#container for holding all the coordinates each segment of the snake 
class SnakeSegment:
	def __init__(self):
		self.pos_x = 0 
		self.pos_y = 0
	
class GameEngine:

	#initialize all the values that will be used  
	def __init__ (self):
		self.segments = 5 #Number of starting segments (Must make a variable for this instand of hard coding it)
		self.snk = [SnakeSegment() for i in range(self.segments)]
		self.nextpos = SnakeSegment()
		self.nextpos.pos_x = -1
		self.nextpos.pos_y = 0

		for i in range(0,self.segments):
			self.snk[i].pos_x = i+10
			self.snk[i].pos_y = 5
			
		self.key = "Right"
		self.points = 0
		self.coin = Coin() #initialze the class for COIN
	
	
	#self explanatory;check if the player changed the direction and change which way the snake may go
	"""make a tuple for the key inputs"""
	def get_direction (self):
		self.key = getHeldKeys()
		if "Left" in self.key:
			self.nextpos.pos_x = -1
			self.nextpos.pos_y = 0
		elif "Right" in self.key:
			self.nextpos.pos_x = 1
			self.nextpos.pos_y = 0
		elif "Down" in self.key:
			self.nextpos.pos_x = 0
			self.nextpos.pos_y = 1
		elif "Up" in self.key:
			self.nextpos.pos_x = 0
			self.nextpos.pos_y = -1
			
	def move_snake (self):
		self.copy_segments() #update positions of all the segments 
		self.snk[0].pos_x += self.nextpos.pos_x #update the x position of the the head
		self.snk[0].pos_y += self.nextpos.pos_y #update the y position of the head 
		#self.caught_coin()#check if the new position of the snake caught the coin 
		return self.snake_crashed()#Check if the new position of the snake is invalid (out of bounds or crashed into itself)
	
	#since each segment of snake follows the segment infront of it, this function will copy the x and y position of the next segment
	#to previous
	def copy_segments(self):
		for i in range (self.segments-1,0,-1):
			self.snk[i].pos_x = self.snk[i-1].pos_x
			self.snk[i].pos_y = self.snk[i-1].pos_y
	
	#debugging purposes 
	#def show_pos(self):
		#for i in range(0,self.segments):
			#print ("position x: ",self.snk[i].pos_x, "position y: ",self.snk[i].pos_y)	
	
	#self explanatory, appends a new object (segment) to the list of existing segments
	def add_segment (self):
		self.segments = self.segments + 1
		self.snk.extend([SnakeSegment()])
	
	#Checck to see wether the snake "caught" the coin 
	def caught_coin (self):
		if self.snk[0].pos_x == self.coin.pos_x and self.snk[0].pos_y == self.coin.pos_y:
			self.points = self.points + 100
			self.coin.update_coin()
			self.add_segment()
	
	#Check to see if the snake has either crashed into itself or is out of bound
	def snake_crashed (self):
		#check if snake head is out of bounds
		if (self.snk[0].pos_x > MAXX or self.snk[0].pos_x < MINX )  or (self.snk[0].pos_y > MAXY or self.snk[0].pos_y < MINY):
			return True
		#check if the head of snake crashed into itself
		for i in range (1,self.segments):
			if self.snk[0].pos_x == self.snk[i].pos_x and self.snk[0].pos_y == self.snk[i].pos_y:
				return True
				
				
	#Self explanatory;redraw the frame
	def update_graphics(self):		
		clear()
		rect(self.coin.pos_x*ZOOM,self.coin.pos_y*ZOOM,HEIGHT,WIDTH)
		for i in range (0,self.segments):
			rect(self.snk[i].pos_x*ZOOM,self.snk[i].pos_y*ZOOM,HEIGHT,WIDTH)
		
		update()

resize (MAXX*ZOOM,MAXY*ZOOM) #Resize the window
setAutoUpdate(False)		
background(0,0,0)#Set background to black 
		
def main ():
	game = GameEngine()
	crashed = False
	#setFont("System", "24", "bold")
	#text (25*ZOOM,25*ZOOM,"Welcome to the game of snake!")
	
	#set the colour of the snake
	setOutline (255,255,255)
	setFill(255,255,255)
	
	#Main loop
	while not(closed()):
		sleep (1/30)
		game.get_direction()
		game.caught_coin()
		crashed = game.move_snake()	
		if crashed == True:
			break
		else:
			game.update_graphics()

main ()	
print("hee")
	


