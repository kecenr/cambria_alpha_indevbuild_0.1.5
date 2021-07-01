import pygame
from config import *
import sys
import math
import time
import random

class spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = p_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        pygame.mixer.pre_init(44100, 16, 2, 32) #frequency, size, channels, buffersize

        self.x = x * TileSize
        self.y = y * TileSize
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.an_loop = 0
        self.footstep_timer = 0

        self.width = TileSize
        self.height = TileSize

        self.image = self.game.playerspritesheet.get_sprite(0, 0, 32, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hp = 100

        # loading player sounds

        self.footsteps = [pygame.mixer.Sound('Assets/footstep1.mp3'),
                                   pygame.mixer.Sound('Assets/footstep2.mp3'),
                                   pygame.mixer.Sound('Assets/footstep3.mp3'),
                                   pygame.mixer.Sound('Assets/footstep4.mp3')]

    def update(self):
        self.movement()
        self.animation()
        self.rect.x += self.x_change
        self.collision('x')
        self.rect.y += self.y_change
        self.collision('y')
        self.enemy_collision()

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()

        if self.footstep_timer > 0:
            self.footstep_timer -= 1

        if self.footstep_timer == 0:
            self.footstep_timer = 20

        if keys[pygame.K_w]:

            self.y_change -= PlayerVel
            self.facing = 'up'

            if self.footstep_timer == 20:
                random.choice(self.footsteps).play()

        if keys[pygame.K_a]:

            self.x_change -= PlayerVel
            self.facing = 'left'

            if self.footstep_timer == 20:
                random.choice(self.footsteps).play()

        if keys[pygame.K_s]:

            self.y_change += PlayerVel
            self.facing = 'down'

            if self.footstep_timer == 20:
                random.choice(self.footsteps).play()

        if keys[pygame.K_d]:

            self.x_change += PlayerVel
            self.facing = 'right'

            if self.footstep_timer == 20:
                random.choice(self.footsteps).play()

    #collisions

    def collision(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def enemy_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            
        if hits:
            self.hp -= 20
            if self.hp < 0:
                self.kill()
                self.game.playing = False

    def mct_collision(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, map_change_trigger, False)
            if hits:
                if self.x_change > 0:
                    self.tilemap = self.tilemap.links[(x,y)]
                if self.x_change < 0:
                    self.tilemap = self.tilemap.links[(x,y)]

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.tilemap = self.tilemap.links[(x,y)]
                if self.y_change < 0:
                    self.tilemap = self.tilemap.links[(x,y)]

    def animation(self):

        right_walk = [self.game.playerspritesheet.get_sprite(64, 0, self.width, self.height), # left foot
                             self.game.playerspritesheet.get_sprite(32, 0, self.width, self.height)] # right foot

        left_walk = [self.game.playerspritesheet.get_sprite(128, 0, self.width, self.height), # left foot
                           self.game.playerspritesheet.get_sprite(160, 0, self.width, self.height)] # right foot

        down_walk = [self.game.playerspritesheet.get_sprite(224, 0, self.width, self.height), # left foot
                             self.game.playerspritesheet.get_sprite(256, 0, self.width, self.height)] # right foot

        up_walk = [self.game.playerspritesheet.get_sprite(320, 0, self.width, self.height), # left foot
                         self.game.playerspritesheet.get_sprite(352, 0, self.width, self.height)] # right foot

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.playerspritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = right_walk[math.floor(self.an_loop)]
                self.an_loop += 0.1 # determines animation speed
                if self.an_loop >= 2: # resets the animation
                    self.an_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.playerspritesheet.get_sprite(96, 0, self.width, self.height)
            else:
                self.image = left_walk[math.floor(self.an_loop)]
                self.an_loop += 0.1 # determines animation speed
                if self.an_loop >= 2: # resets the animation
                    self.an_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.playerspritesheet.get_sprite(192, 0, self.width, self.height)
            else:
                self.image = down_walk[math.floor(self.an_loop)]
                self.an_loop += 0.1 # determines animation speed
                if self.an_loop >= 2: # resets the animation
                    self.an_loop = 0

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.playerspritesheet.get_sprite(288, 0, self.width, self.height)
            else:
                self.image = up_walk[math.floor(self.an_loop)]
                self.an_loop += 0.1 # determines animation speed
                if self.an_loop >= 2: # resets the animation
                    self.an_loop = 0

# game elements

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Assets/PixelOperator-Bold.ttf', 32)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self._layer = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class hud (pygame.sprite.Sprite):
    def __init__(self, game, hudx, hudy):

        self.game = game
        self._layer = 3
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.hudx = 0
        self.hudy = 0

        self.width = WinWidth
        self.height = 80
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(black)
        self.rect = self.image.get_rect()

        # Unimplemented (broken) code for a HP system

        #self.hpdisplay = Button(10, 100, 100, 50, white, black, 'HP: {n}', 32) #.format(n=game.player.hp), 32)
        #self.hpdisplay = game.font.render('HP: 100', True, white)
        #self.hpdisplay.rect = self.hpdisplay.get_rect(x=10, y=10)
        #game.screen.blit(self.hpdisplay, self.hpdisplay.rect)

class map_change_trigger(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TileSize
        self.y = y * TileSize
        self.width = TileSize
        self.height = TileSize

        self.image = self.game.grass.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


# enemies

class rover(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = foe_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TileSize
        self.y = y * TileSize
        self.width = TileSize
        self.height = TileSize

        self.x_change = 0
        self.y_change = 0
        self.idle = 0

        self.facing = random.choice(['left', 'right', 'swdash', 'nwdash', 'nedash', 'sedash', 'idle'])
        self.move_loop = 0
        self.max_travel = random.randint(32, 128)
        self.max_dash = random.randint(32, 64)

        self.image = self.game.roverspritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        self.movement()
        self.animation()
        self.collision()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        if self.facing == 'left':
            self.x_change -= RoverVel
            self.move_loop -= 1
            if self.move_loop <= -self.max_travel:
                self.facing = random.choice(['right', 'swdash', 'nwdash', 'nedash', 'sedash', 'idle'])

        elif self.facing  == 'right':
            self.x_change += RoverVel
            self.move_loop += 1
            if self.move_loop >= self.max_travel:
                self.facing = random.choice(['left', 'swdash', 'nwdash', 'nedash', 'sedash', 'idle'])

        elif self.facing  == 'swdash':
            self.x_change -= RoverDashVel
            self.y_change += RoverDashVel
            self.move_loop += 1
            if self.move_loop >= self.max_dash:
                self.facing = random.choice(['left', 'right', 'nwdash', 'nedash', 'sedash', 'idle'])

        elif self.facing  == 'sedash':
            self.x_change += RoverDashVel
            self.y_change += RoverDashVel
            self.move_loop += 1
            if self.move_loop >= self.max_dash:
                self.facing = random.choice(['left', 'right', 'nwdash', 'nedash', 'swdash', 'idle'])

        elif self.facing  == 'nwdash':
            self.x_change -= RoverDashVel
            self.y_change -= RoverDashVel
            self.move_loop += 1
            if self.move_loop >= self.max_dash:
                self.facing = random.choice(['left', 'right', 'sedash', 'nedash', 'swdash', 'idle'])

        elif self.facing  == 'nedash':
            self.x_change += RoverDashVel
            self.y_change -= RoverDashVel
            self.move_loop += 1
            if self.move_loop >= self.max_dash:
                self.facing = random.choice(['left', 'right', 'sedash', 'nwdash', 'swdash', 'idle'])

        elif self.facing == 'idle':
            self.idle += 1
            self.x_change = 0
            self.y_change = 0
            self.move_loop = 0
            if (self.idle > 100):
                self.facing = random.choice(['left', 'right', 'swdash', 'nwdash', 'nedash', 'sedash'])

    def animation(self):

        if self.facing == 'right' or self.facing == 'nedash' or self.facing == 'sedash':
            self.image = self.game.roverspritesheet.get_sprite(32, 0, self.width, self.height)

        elif self.facing == 'left' or self.facing == 'swdash' or self.facing == 'nwdash':
            self.image = self.game.roverspritesheet.get_sprite(64, 0, self.width, self.height)

        elif self.facing == 'idle':
            self.image = self.game.roverspritesheet.get_sprite(0, 0, self.width, self.height)

    def collision(self):

#credit to belambic for coding most of this

        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.move_loop = 0
            if self.x_change < 0:
                if self.y_change < 0:
                    self.facing = random.choice(['right', 'sedash'])
                elif self.y_change == 0:
                    self.facing = random.choice(['right', 'nedash', 'sedash'])
                elif self.y_change > 0:
                    self.facing = random.choice(['right', 'nedash'])
            elif self.x_change > 0:
                if self.y_change < 0:
                    self.facing = random.choice(['left', 'swdash'])
                elif self.y_change == 0:
                    self.facing = random.choice(['left', 'nwdash', 'swdash'])
                elif self.y_change > 0:
                    self.facing = random.choice(['left', 'nwdash'])
            self.x_change = -self.x_change
            self.y_change = -self.y_change

    def entity_collision(self):

# I had to copy the block collision code because for some reason  you can only put one sprite group in the
# hits variable or else it sets the last argument to True which makes the blocks disappear.

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.move_loop = 0
            if self.x_change < 0:
                if self.y_change < 0:
                    self.facing = random.choice(['right', 'sedash'])
                elif self.y_change == 0:
                    self.facing = random.choice(['right', 'nedash', 'sedash'])
                elif self.y_change > 0:
                    self.facing = random.choice(['right', 'nedash'])
            elif self.x_change > 0:
                if self.y_change < 0:
                    self.facing = random.choice(['left', 'swdash'])
                elif self.y_change == 0:
                    self.facing = random.choice(['left', 'nwdash', 'swdash'])
                elif self.y_change > 0:
                    self.facing = random.choice(['left', 'nwdash'])
            self.x_change = -self.x_change
            self.y_change = -self.y_change

# tiles

class block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TileSize
        self.y = y * TileSize
        self.width = TileSize
        self.height = TileSize

        self.image = self.game.stonebricks.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class grass(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TileSize
        self.y = y * TileSize
        self.width = TileSize
        self.height = TileSize

        self.image = self.game.grass.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
