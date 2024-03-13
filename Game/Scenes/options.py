from .scene import Scene
import pygame
from pygame.locals import *

class Settings(Scene):
    def __init__(self, director):
        super(Settings, self).__init__(director)
        self.menu = ['Music Volume', 'Sound Effects Volumen', 'RETURN']

        self.music_slider = Slider(self.screen_rect.center, (300,30), 0, self.director.music_volume)
        self.effects_slider = Slider(self.screen_rect.center, (300,30), 1, self.director.sounds_volume)

        self.return_color = pygame.Color('white')

        self.mouse_pos = {
            'CLICKED': (0,0),
            'HOVER': (0,0)
        }
        self.return_rect = pygame.Rect(0,0,0,0)

    def render_text(self, index):
        if index == 2:
            rendered_option = self.font.render(self.menu[index], True, self.return_color)
            self.return_rect = rendered_option.get_rect(center=(self.screen_rect.center[0], self.screen_rect.center[1] + (index * 150)))
        else:
            rendered_option = self.font.render(self.menu[index], True, pygame.Color('white'))
        return rendered_option
    
    def get_text_position(self, surface, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 150))
        return surface.get_rect(center=center)

    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pos['CLICKED'] = event.pos
            elif event.type == MOUSEMOTION:
                self.mouse_pos['HOVER'] = event.pos

    def update(self, dt):
        music_volume = self.music_slider.get_value()
        sounds_volume = self.effects_slider.get_value()
        if self.music_slider.container_rect.collidepoint(self.mouse_pos['CLICKED']):
            self.music_slider.move_slider(self.mouse_pos['CLICKED'])
            pygame.mixer.music.set_volume(music_volume)

        if self.effects_slider.container_rect.collidepoint(self.mouse_pos['CLICKED']):
            self.effects_slider.move_slider(self.mouse_pos['CLICKED'])

        if self.return_rect.collidepoint(self.mouse_pos['HOVER']):
            self.return_color = pygame.Color('blue')
        else:
            self.return_color = pygame.Color('white')
        if self.return_rect.collidepoint(self.mouse_pos['CLICKED']):
            if music_volume < 0.1:
                self.director.music_volume = 0.0
            else:
                self.director.music_volume = music_volume
            if sounds_volume < 0.1:
                self.director.sounds_volume = 0.0
            else:
                self.director.sounds_volume = sounds_volume
            self.director.finishScene()


    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        for index, item in enumerate(self.menu):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))
            if item == 'Music Volume':
                self.music_slider.render(surface)
            if item == 'Sound Effects Volumen':
                self.effects_slider.render(surface)


class Slider():
    def __init__(self, pos, size, place, sliderPos):
        self.x = pos[0] - (size[0]//2)
        self.tx = pos[0] + (size[0]//2)
        self.y = pos[1] + 50 + place*150
        self.w = size[0]
        self.h = size[1]

        self.container_rect = pygame.Rect(self.x, self.y, size[0], size[1])
        self.button_rect = pygame.Rect(self.x + self.w*sliderPos,self.y,10,self.h)

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self, surface):
        pygame.draw.rect(surface, 'darkgray', self.container_rect)
        pygame.draw.rect(surface, 'blue', self.button_rect)

    def get_value(self):
        val_range = self.tx - self.x
        button_val = self.button_rect.centerx - self.x

        return (button_val/val_range)