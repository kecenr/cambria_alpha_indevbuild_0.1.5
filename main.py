#main

import pygame
from entitydata import *
from config import *
from leveldata import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WinWidth, WinHeight), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.mixer.pre_init(44100, 16, 2, 32) #frequency, size, channels, buffersize
        self.title = pygame.display.set_caption('Cambria')
        self.iconpng = pygame.image.load('Assets/icon.png')
        self.icon = pygame.display.set_icon(self.iconpng)
        self.running = True
        self.font = pygame.font.Font('Assets/PixelOperator-Bold.ttf', 32)
        self.tilemap = tilemap01()
        world_data = []

        # loading images

        self.playerspritesheet = spritesheet('Assets/playerspritesheet.png')
        self.grass = spritesheet('Assets/grass.png')
        self.stonebricks = spritesheet('Assets/stonebricks.png')
        self.roverspritesheet = spritesheet('Assets/roverspritesheet.png')
        self.intro_background = pygame.image.load('Assets/gradient.png')
        self.gameover_background = pygame.image.load('Assets/gameover.png')

        # loading sound and music

        self.titlescreenmusic = pygame.mixer.music.load('Assets/gymnopedie.wav')
        self.death_sound = pygame.mixer.Sound('Assets/death.wav')

    def TileCreate(self, tilemap):
    
        for i, row in enumerate(self.tilemap.mapdata):
            for j, column in enumerate(row):
                grass(self, j, i)
                if column == '1':
                    block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)
                if column == 'R':
                    rover(self, j, i)
                if column == 'T':
                    map_change_trigger(self, j, i)

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tiles = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.hud = hud(self, 0, 0)

        self.TileCreate(self.tilemap)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        

    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('You have tragically passed away.', True, white)
        text_rect = text.get_rect(x=10, y=10)
        
        continue_button = Button(10, 100, 140, 50, white, black, 'Continue?', 32)

        self.death_sound.play()

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.gameover_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            

    def intro_screen(self):
        intro = True

        title = self.font.render('Cambria', True, white)
        title_rect = title.get_rect(x=10, y=10)
        pygame.mixer.music.play(-1)

        play_button = Button(-5, 100, 100, 50, white, black, 'PLAY', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.mixer.music.fadeout(500)
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
    
