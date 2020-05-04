import pygame
import math
from pygame.locals import *
from random import randint

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

#Key mapping
keys = {
	"top": False,
	"bottom": False,
	"left": False,
	"right": False
}

running = True

playerpos = [100, 100] #Inisialisasi pos untuk pemain

score = 0
arrows = []

health_point = 194 #Default health point untuk kastil
countdown_timer = 90000 #90 detik

enemy_timer = 100 #Waktu kemunculan
enemies = [[width, 100]] #List yang menampung koordinat musuh

#Load aset game
#Load image

player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

#Game loop
while(running):

	#Clear screen
	screen.fill(0)

	#Draw game object
	

	#Draw grass
	for x in range(int(width/grass.get_width()+1)):
		for y in range(int(height/grass.get_height()+1)):
			screen.blit(grass, (x*100, y*100))

	#Draw the castle
	screen.blit(castle, (0, 30))
	screen.blit(castle, (0, 135))
	screen.blit(castle, (0, 240))
	screen.blit(castle, (0, 345))

	mouse_position = pygame.mouse.get_pos()
	angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
	player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
	new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
	screen.blit(player_rotation, new_playerpos)

	for bullet in arrows:
		arrow_index = 0
		velx=math.cos(bullet[0])*10
		vely=math.sin(bullet[0])*10
		bullet[1]+=velx
		bullet[2]+=vely
		if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
			arrows.pop(arrow_index)
		arrow_index += 1

		#Draw arrow
	for projectile in arrows:
		new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
		screen.blit(new_arrow, (projectile[1], projectile[2]))

	#Draw enemy
	enemy_timer -= 1
	if enemy_timer == 0:
		#Buat musuh baru
		enemies.append([width, randint(50, height-32)])
		#Reset enemy timer
		enemy_timer = randint(1, 100)

	#Draw health bar
	screen.blit(healthbar, (5,5))
	for hp in range(health_point):
		screen.blit(health, (hp+8, 8))

	#Draw clock
	font = pygame.font.Font(None, 24)
	minutes = int((countdown_timer-pygame.time.get_ticks())/60000)
	seconds = int((countdown_timer-pygame.time.get_ticks())/1000*60)
	time_text = "{:02}:{:02}".format(minutes, seconds)
	clock = font.render(time_text, True, (255,255,255))
	textRect = clock.get_rect()
	textRect.topright = [635, 5]
	screen.blit(clock, textRect)

	index = 0
	for enemy in enemies:
		#Musuh bergerak dengan kecepatan  pixel ke kiri
		enemy[0] -= 5
		#Hapus musuh saat mencapai batas layar sebelah kiri
		if enemy[0] < -64:
			enemies.pop(index)

	enemy_rect = pygame.Rect(enemy_img.get_rect())
	enemy_rect.top = enemy[1]
	enemy_rect.left = enemy[0]

	if enemy_rect.left < 64:
		enemies.pop(index)
		health_point -= randint(5, 20)
		print("Sial! Aku teserang pok ne ah!")

	index_arrow = 0
	for bullet in arrows:
		bullet_rect = pygame.Rect(arrow.get_rect())
		bullet_rect.left = bullet[1]
		bullet_rect.top = bullet[2]

		if enemy_rect.colliderect(bullet_rect):
			score += 1
			enemies.pop(index)
			arrows.pop(index_arrow)
			print("Boom! Pelot kamu!")
			print("Score: {}".format(score))
		index_arrow += 1
	index += 1

	#Gambar musuh ke layar
	for enemy in enemies:
		screen.blit(enemy_img, enemy)

	#Update screen
	pygame.display.flip()

	#Event loop
	for event in pygame.event.get():
		#Even saat tombol diklik
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)

		if event.type == pygame.MOUSEBUTTONDOWN:
			arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])

		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys["top"] = True
			elif event.key == K_a:
				keys["left"] = True
			elif event.key == K_s:
				keys["bottom"] = True
			elif event.key == K_d:
				keys["right"] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys["top"] = False
			elif event.key == K_a:
				keys["left"] = False
			elif event.key == K_s:
				keys["bottom"] = False
			elif event.key == K_d:
				keys["right"] = False

				# End of event loop

				#9 Move player
				if keys["top"]:
					playerpos[1] -= 5 #kurangi nilai y
				elif keys["bottom"]:
					playerpos[1] += 5 #Tambah nilai y
				elif keys["left"]:
					playerpos[0] -= 5 #kurang nilai x
				elif keys["right"]:
					playerpos[0] += 5 #tambah nilai x
