
from pygame import *
from random import *

mixer.init()

WIDTH = 700
HEIGHT = 500

root = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Shooter')
background = transform.scale(image.load ('galaxy.jpg'), (WIDTH, HEIGHT))
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, image_src, x, y, w, h, speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(image_src), (w, h))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def redraw(self):
        root.blit(self.image, (self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def update(self):
        global HEIGHT
        self.rect.y -= self.speed
        if self.rect.y > HEIGHT:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a])and self.rect.x > 0 :
            self.rect.x -= self.speed
        elif (keys[K_RIGHT] or keys[K_d]) and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
    def fire(self):
        bul = Bullet('bullet.png', ship.rect.x, ship.rect.y, 10, 5, 5)
        bullets.add(bul)

Asters1 = sprite.Group()

loss = 0
class Enemy(GameSprite):
    def update(self):
        global HEIGHT
        global WIDTH
        global loss
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            loss +=1
            self.rect.y = 0
            self.rect.x = randint(0+10, WIDTH-50)

class Aster(GameSprite):
    def update(self):
        global HEIGHT
        global WIDTH
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.speed = 0

from time import time as timer

start_time = timer()
endtime = start_time

clock = time.Clock()

monsters = sprite.Group()
for i in range (5):
    mob = Enemy('ufo.png', randint(0, WIDTH-50), -40, 80, 50, randint(1, 8))
    monsters.add(mob)
bullets = sprite.Group()


monsters.draw(root)
monsters.update()

ship = Player('rocket.png', 5, 400, 80, 100, 10)

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

finish = False

game_on = True
win_count = 0


font.init()
font1 = font.SysFont('arial',36)
font2 = font.SysFont('arial',50)
while game_on:  
    for e in event.get():
        if e.type == QUIT:
            game_on = False
        if e.type == KEYDOWN:
            if e.key == K_f:
                ship.fire()

    if (endtime - start_time) >= 10:
        ast = Aster(mob,randint(0, WIDTH-50), -40, 80, 50, 5)
        Asters1.add(ast)
        start_time = timer()

    endtime = timer()

                
    if not finish:
        root.blit(background,(0,0))
        text_lose = font1.render('Пропущено:' + str(loss), 1, (255,255,255))
        text_win = font1.render('расстреляно:' + str(win_count), 1, (255,255,255))
        root.blit(text_lose,(10, 0))
        root.blit(text_win,(10, 50))

        sprites_list = sprite.groupcollide( monsters, bullets, True, True)
        for sp in sprites_list:
            win_count += 1
            mob = Enemy('ufo.png', randint(0, WIDTH-50), -40, 80, 50, randint(1, 8))
            monsters.add(mob)

        if win_count > 10:
            finish = True
            text1 = font2.render('Победа! ', 1, (255,255,255))
            root.blit(text1, (150, 200))
        if loss > 3:
            finish = True
            text2 = font2.render('Проиграл! ', 1, (255,255,255))
            root.blit(text2, (100, 100))


        ship.update()
        monsters.update()
        monsters.draw(root)

        ship.redraw()
        bullets.update()
        bullets.draw(root)
        display.update()

    clock.tick(5)
