from email.mime import image
import pydoc
import pygame
from pygame.locals import *
from pygame import mixer
import levels

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fsp = 60
t=0
screen_width = 1000
screen_height = 600

font = pygame.font.SysFont('calibri', 30)
white = (255,255,255)

#load sons
pygame.mixer.music.load('./img/song.mpeg')

pygame.mixer.music.play(-1, 0.0, 5000)
jum = pygame.mixer.Sound('img/jump.wav')
jum.set_volume(0.5)
coi = pygame.mixer.Sound('img/coin.wav')
coi.set_volume(0.5)
gamr = pygame.mixer.Sound('img/game_over.wav')
gamr.set_volume(0.5)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define game variables
tile_size = 50

game_over = 0

#load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/tet.jpg')
bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))


class Player():
	def __init__(self, x, y):
		self.reset(x,y)

	def update(self,game_over):
		dx = 0
		dy = 0
		walh_cooldown = 20

		#get keypresses
		if game_over==0 :
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jum.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter +=5
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter +=5
				self.direction = 1
			if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			
			if self.counter > walh_cooldown:
				self.counter = 0

				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list :
				if tile[1].colliderect(self.rect.x +dx , self.rect.y,self.width, self.height):
					dx=0
				#direction Y
				if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height):
					if self.vel_y< 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0 :
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, blob2_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, big_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, ex_group, False):
				game_over = 1
			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height
				dy = 0
		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 3
		#draw player onto screen
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255,255,255), self.rect, 2)
		return game_over
	def reset(self,x,y):
		self.images_right = []
		self.images_left = []
		self.index=0
		self.counter = 0
		for num in range(1,5):
			img_right = pygame.image.load(f'img/yarbe{num}.png')
			img_right= pygame.transform.scale(img_right, (40, 80))
			img_left= pygame.transform.flip(img_right,True,False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True




class Enemy(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.img_right= pygame.image.load('img/blob.png')
		
		self.img_left= pygame.transform.flip(self.img_right,True,False)
		self.image = self.img_left
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
		

	def update(self):
		self.rect.x +=self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) >50 :
			self.move_direction *=-1
			self.move_counter *= -1
			if self.move_direction == -1:
				self.image = self.img_right
			elif self.move_direction == 1:
				self.image = self.img_left

class Enemy2(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.img_right= pygame.image.load('img/Enemy2.png')
		
		self.img_left= pygame.transform.flip(self.img_right,True,False)
		self.image = self.img_left
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 2
		self.move_directiony = 2
		self.move_counter = 0
		self.move_countery = 0
		

	def update(self):
		self.rect.x +=self.move_direction
		self.rect.y +=self.move_directiony
		self.move_counter += 1
		self.move_countery += 1
		if abs(self.move_counter) == 25 :
			self.move_direction *=-1
			self.move_counter *= -1
			if self.move_direction == -2:
				self.image = self.img_right
			elif self.move_direction == 2:
				self.image = self.img_left
		if abs(self.move_countery) == 50 :
			self.move_directiony *=-1
			self.move_countery *= 0


class Bigenemy(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		big_img = pygame.image.load('img/en1.png')
		self.image = pygame.transform.scale(big_img,(50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y-50
		self.move_direction = 1
		self.move_directiony = 1
		self.move_counter = 0
		self.move_countery = 0


	def update(self):
		self.rect.x +=self.move_direction
		self.rect.y +=self.move_directiony
		self.move_counter += 1
		self.move_countery += 1

		if abs(self.move_counter) >50 :
			self.move_direction *=-1
			self.move_counter *=-1

		if self.move_countery>50:
			self.move_directiony*=-1
			self.move_countery=0


class Lava(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img,(tile_size,tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin2.png')
		self.image = pygame.transform.scale(img,(tile_size-15,tile_size-15))
		self.rect = self.image.get_rect()
		self.rect.center=(x,y)

class Ex(pygame.sprite.Sprite):
	def __init__ (self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img,(tile_size*1.5,tile_size*2.05))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Button():
	def __init__(self,x,y,image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False
	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
				action = True
				self.clicked=True
		if pygame.mouse.get_pressed()[0]==0:
			self.clicked=False


		screen.blit(self.image, self.rect)
		return action


class World():
	def __init__(self, data):
		self.res(data)
	def res(self,data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')
		#ex_img = pygame.image.load('img/exit.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 8:
					'''img = pygame.transform.scale(ex_img, (tile_size*2, tile_size*2))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)'''
					ex = Ex(col_count * tile_size + 15, row_count * tile_size)
					ex_group.add(ex)
				if tile == 3:
					blob = Enemy(col_count * tile_size , row_count * tile_size +15)
					blob_group.add(blob)
				if tile == 7:
					blob2 = Enemy2(col_count * tile_size , row_count * tile_size +15)
					blob2_group.add(blob2)
				if tile == 4:
					big = Bigenemy(col_count * tile_size , row_count * tile_size)
					big_group.add(big)
				if tile == 5:
					coin = Coin(col_count *tile_size + tile_size//2, row_count * tile_size + (tile_size//2))
					coin_group.add(coin)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size//2))
					lava_group.add(lava)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], (tile[1].x , tile[1].y))
	def draw2(self):
		for tile in self.tile_list:
			screen.blit(tile[0], (tile[1].x , tile[1].y))

			#pygame.draw.rect(screen, (255,255,255), tile[1], 2)
	


#[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]



def reset_level(lev):
	player.reset(100, screen_height - 130)
	big_group.empty()
	blob_group.empty()
	blob2_group.empty()
	lava_group.empty()
	ex_group.empty()
	world_data=levels.world_data[lev]
	world=World(world_data)
	return world

def text(text,font,col,x,y):
	img = font.render(text, True, col)
	screen.blit(img,(x,y))



player = Player(100, screen_height - 130)

level=0
score = 0

coin_group = pygame.sprite.Group()
big_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
blob2_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
ex_group = pygame.sprite.Group()
world_data = levels.world_data[level]
world = World(world_data)
res_img = pygame.image.load('img/restart_btn.png')
res_img = pygame.transform.scale(res_img,(150,60))
res = Button(screen_width//2 -100 , screen_height//2  , res_img )


exit_img = pygame.image.load("img/exit_btn.png")
exit_img = pygame.transform.scale(exit_img,(150,70))
exit = Button(screen_width//2+50,screen_height//2+100, exit_img)

str_img = pygame.image.load("img/start_btn.png")
str_img = pygame.transform.scale(str_img,(150,70))
strt = Button(screen_width//2-200,screen_height//2+100, str_img)

run = True
menu = True
while run:
	clock.tick(fsp)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (500, 150))
	
	if menu:
		if exit.draw():
			run = False
		if strt.draw():
			menu=False
	else:
		world.draw()
		if game_over == 0:
			blob_group.update()
			blob2_group.update()
			big_group.update()
			if pygame.sprite.spritecollide(player, coin_group, True):
				coi.play()
				score += 1
			text('score : ' + str(score), font, "black",100,0)
		
		coin_group.draw(screen)
		blob_group.draw(screen)
		blob2_group.draw(screen)
		lava_group.draw(screen)
		
		ex_group.draw(screen)
		big_group.draw(screen)
		game_over = player.update(game_over)
		if game_over == -1:
			gamr.play()
			hjhj=pygame.font.SysFont('arial',70).render('you lose', True, "blue")
			screen.blit(hjhj,(300,100))
			if res.draw():
				player.reset(100, screen_height - 130)
				game_over=0
		if game_over == 1:
			level+=1
			if level < len(levels.world_data):

				world_data=[]
				world = reset_level(level)
				game_over=0
			else:
				hjhj=pygame.font.SysFont('calibri',50).render('you win', True, (255,0,0))
				screen.blit(hjhj,(300,100))
				if res.draw():
					
					level=0
					world_data=[]
					world = reset_level(level)
					game_over=0
					

				
		#win.draw()
		#screen.blit(win_img,(300,0))
		#print(game_over)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()
