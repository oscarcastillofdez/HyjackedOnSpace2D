import pygame

class UIText():
    def __init__(self, gv) -> None:
        self.font = pygame.font.Font(None, 96)
        self.surfaceText = None
        self.globalVars = gv
        self.surfaceText = self.font.render("", True, "black")


    def setInteractualeText(self, text, color):
        self.surfaceText = self.font.render(text, True, color)

    def update(self, observable):
        self.setInteractualeText(observable.getInteractuableText(), "black")
        
    def draw(self, screen):
        screen.blit(self.surfaceText, (self.globalVars.SCREEN_WIDTH / 2, self.globalVars.SCREEN_HEIGTH / 2))
        
