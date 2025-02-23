import pygame

pygame.init()
pygame.display.set_mode((1,1))

pygame.key.set_repeat(100, 100)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				print 'go forward'
			if event.key == pygame.K_s:
				print 'go backward'
		if event.type == pygame.KEYUP:
			print 'stop'
