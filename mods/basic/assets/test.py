import pygame, time, spritesheet
sh=spritesheet.Spritesheet(pygame.image.load("player.png"),32)

s=pygame.display.set_mode((128,128))


img0=sh[0] # red
img1=sh[1] # green


img1=pygame.transform.rotate(sh[1],90)

s.blit(img1, (0,0))
s.blit(sh[1],(32,32))


pygame.display.flip()
time.sleep(1.3)
pygame.quit()