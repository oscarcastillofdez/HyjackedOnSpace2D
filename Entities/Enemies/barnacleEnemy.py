import pygame
from Constants.constants import ENEMIES_PATH

from Entities.Enemies.entity import Entity

class BarnacleEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, dificulty, onlyChase) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle.png'), (64,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tongueImage = pygame.transform.scale(pygame.image.load(ENEMIES_PATH + 'Barnacle_tongue.png'), (64,400))
        #self.verticalRect = pygame.Rect(self.rect.centerx,self.rect.centery,10, 400)
        self.tongueRect = self.tongueImage.get_rect()
        self.tongueRect.x = self.rect.x
        self.tongueRect.y = self.rect.y
        self.tongueRect.width = 10
        self.tongueRect.height = 400

        self.damage = dificulty.getBarnacleEnemyDamage()

        # Atributos de vida
        self.health = dificulty.getBarnacleEnemyHealth()

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "die": self.die}
        self.current_state = "patrolling"
    
    def update(self, dt, world, player,cameraOffset, enemies_group):
        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        self.tongueRect.x = self.rect.x
        self.tongueRect.y = self.rect.y

        self.states[self.current_state](world, player, cameraOffset, enemies_group) # Llama al estado correspondiente (patrol, chase o attack)

    def patrol(self, world, player,cameraOffset,enemies_group):
        if self.tongueRect.colliderect(player.position()):
            self.current_state = "chasing"
    
    def chase(self, world, player,cameraOffset,enemies_group):
        player.setGrabbed(1, self.rect)
        
        if self.rect.colliderect(player.position()):
            self.current_state = "attacking"

    def die(self,world, player,cameraOffset,enemies_group):
        player.unSetGrabbed()
        enemies_group.remove(self)

    def attack(self, world, player,cameraOffset,enemies_group):
        player.setGrabbed(0,self.rect)
        player.hit(self.damage)
    
    def drawBullets(self,screen):
        #pygame.draw.rect(screen, (255,255,255), self.verticalRect)
        screen.blit(self.tongueImage, self.tongueRect)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.current_state = "die"
    
