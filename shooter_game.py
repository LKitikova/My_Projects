#Создай собственный Шутер!

from pygame import *
from random import randint

w = 700
h = 500 

FPS = 60
clock = time.Clock()

game = True
finish = False

windows = display.set_mode((w,h))
display.set_caption("Game")

score = 0
lost = 0

#группы: монстры и пули
monsters = sprite.Group()
shots = sprite.Group()
aster = sprite.Group()

#фон
backgraund = transform.scale(image.load("galaxy.jpg"),(w,h))

#музыка фон
mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()

#единичная музыка
music_fire = mixer.Sound("fire.ogg")

#подключить шрифты
font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 36)

#надпись победы 
win = font1.render("YOU WIN!", True, (255, 215, 0)) #желтый
#надпись поражения
lose = font1.render("YOU LOSE!", True, (255, 0, 0)) #красный
#надпись счетчика
scorelable = font2.render("Счет:" + str(score), 1, (255, 255, 255)) #белый
#надпись пропущенно
lostlable = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255)) #белый

class GameSprite(sprite.Sprite):
    def __init__(self, playimage, x, y, speed, size_x, size_y):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(playimage),(self.size_x, self.size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))
    def move_x(self):
        self.rect.x += self.speed
    def move_y(self):
        self.rect.y += self.speed

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_LEFT] and player.rect.x >= 0:
            player.rect.x -= player.speed
        if key_pressed[K_RIGHT] and player.rect.x <= w-65:
            player.rect.x += player.speed

    def Fire(self):
        shot = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 15, 20)
        shots.add(shot)

class Enemy(GameSprite):
    global finish
    
    
    def update(self):
        global lost
        if self.rect.y < h:
            self.rect.y += self.speed
        else:
            self.rect.y = 0 
            self.speed = randint(1, 3)
            self.rect.x = randint(0, w-65)
            lost = lost + 1
            
    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()

class Asteroid(Enemy):
     def update(self):
        global lost
        if self.rect.y < h:
            self.rect.y += self.speed
        else:
            self.rect.y = 0 
            self.speed = randint(1, 3)
            self.rect.x = randint(0, w-65)
    
               

player = Player("rocket.png", w/2, h-65, 7, 65, 65)

for i in range(5):
    randX = randint(0, w-65)
    randSpeed = randint(3, 5)

    agryberds = Enemy("ufo.png", randX, 0, randSpeed, 65, 65)

    monsters.add(agryberds)

for i in range(2):
    randX = randint(0, w-65)
    randSpeed = randint(1,3)

    asteroid = Asteroid("asteroid.png", randX, 0, randSpeed, 65, 65)

    aster.add(asteroid)

#money = GameSprite("treasure.png", 0.9*w, 0.9*h, 0)

#игровой цикл
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN: 
            if i.key == K_SPACE:
                player.Fire()
                music_fire.play()

    windows.blit(backgraund, (0,0))
    
    if finish != True:
        scorelable = font2.render("Счет:" + str(score), 1, (255, 255, 255)) #белый
        lostlable = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255)) #белый
        if lost >= 10:
            finish = True
            windows.blit(lose, (200,200))


        windows.blit(scorelable, (10,20))
        windows.blit(lostlable, (10,50))

        collides = sprite.groupcollide(monsters, shots, True, True)
        
        if  sprite.spritecollide(player, monsters, False):
            finish = True
            windows.blit(lose, (200,200))
            
        for i in collides:
            randX = randint(0, w-65)
            randSpeed = randint(1, 3)
            score += 1
            


            agryberds = Enemy("ufo.png", randX, 0, randSpeed, 65, 65)

            monsters.add(agryberds)

        player.update()
        monsters.update()
        shots.update()
        aster.update()

        player.reset()
        monsters.draw(windows)
        shots.draw(windows)
        aster.draw(windows)

        display.update()

        time.delay(50)

    clock.tick(FPS)