import pygame
from .PlayerStates.idle import Idle, IdleShoot
from .PlayerStates.run import Run, RunShoot
from .PlayerStates.jump import Jump, JumpShoot
from .playerAbstract import PlayerAbstract
from Entities.bullet import Bullet
from Constants.constants import *

# Esta clase es exactamente igual a playerWithPistol, lo unico que cambia es:
# La bala hace +2 de daño
# El sprite de la bala es distinto (Bala verde)
class PlayerWithPistolUpgrade(PlayerAbstract):
    def __init__(self, player, ui):
        super().__init__(player.position().x, player.position().y, player.getDificulty())
        self.player = player

        self.disparoImg = pygame.transform.scale(pygame.image.load(PLAYER_PATH + 'lazer_2.png'), (100,100))
        self.bulletDamageUpgraded = self.bulletDamage + 2

        self.shootCooldown = self.shootCooldownConst        
        # Imagenes
        self.states = {
            "IDLE": Idle(True),
            "RUN": Run(True),
            "JUMP": Jump(True),
            "IDLE-SHOOT": IdleShoot(),
            "JUMP-SHOOT": JumpShoot(),
            "RUN-SHOOT": RunShoot()
        }
        """
            "IDLE": Idle(False),
            "RUN": Run(True),
            "RUN-SHOOT": RunShoot(),
            "RUN-SHOOT-DIAG-UP": RunShootDiagUp(),
            "RUN-SHOOT-DIAG-DOWN": RunShootDiagDown(),
            "RUN-SHOOT-DOWN": RunShootDown(),
            "RUN-SHOOT-UP" : RunShootUp(),
            "IDLE-SHOOT": IdleShoot(),
            "IDLE-SHOOT-UP": IdleShoot(),
            "IDLE-SHOOT-DOWN": IdleShoot(),
            "IDLE-SHOOT-DIAG-UP": IdleShoot(),
            "IDLE-SHOOT-DIAG-DOWN": IdleShoot(),
            "JUMP-SHOOT": JumpShoot(),
            "JUMP": Jump(True)
        """

        self.anim = 0
        self.state_name = "IDLE"
        self.state = self.states[self.state_name]
        self.standing = self.state.get_initial()
        self.deadImage = pygame.transform.rotate(self.standing,90)
        self.hitImage = pygame.transform.rotate(self.standing,90)

        # SoundEffects
        self.shootEffect = pygame.mixer.Sound('Assets/Audio/SoundEffects/laserGun.mp3')
        self.shootEffect.set_volume(self.volume)
        ui.uiPistolUpgrade.uIShow()

    def resetPlayerPos(self):
            self.player.resetPlayerPos()
    
    def idle(self):
        self.player.idle()

    def stopShooting(self):
        self.player.stopShooting()

    def getUiText(self):
        return self.player.getUiText()
        
    def getUiHearts(self):
        return self.player.getUiHearts()

    def idle(self):
        self.player.idle()

    def stopShooting(self):
        self.player.stopShooting()

    def move_left(self):
        self.player.move_left()
    
    def move_right(self):
        self.player.move_right()
    
    def jump(self):
        self.player.jump()
    
    def getHp(self):
        return self.player.getHp()
    
    def interact(self, interactuableGroup):
        self.player.interact(interactuableGroup)

    def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset):
        cameraOffset = self.player.update(world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset)
        self.shootCooldown -= 4 * (dt/100)
        
        return cameraOffset
            
    def deflect(self, direction, bulletImage, velocidadBala, damage, posx, posy, bullets_group):
        self.player.deflect(direction, bulletImage, velocidadBala, damage, posx, posy, bullets_group)

    def shootUpdateSprites(self, direction):
        self.player.shootUpdateSprites(direction)

    def shoot(self, direction, bullets_group):
        self.shootUpdateSprites(direction)

        if self.shootCooldown <= 0:
            self.shootEffect.stop()
            self.shootEffect.play()
            self.shootCooldown = self.shootCooldownConst
            disparo = Bullet(self.disparoImg, direction, self.bulletDamage, self.bulletSpeed, self.player.position().x - 40, self.player.position().y - 30, self, self, False)
            bullets_group.add(disparo)
            

    def draw(self, screen):
        self.player.draw(screen)

    def doInteract(self, interactuableGroup):
        self.player.doInteract(interactuableGroup)

    def position(self):
        return self.player.position()
    
    def hit(self, damage):
        return self.player.hit(damage)
    
    def cover(self):
        self.player.cover()

    def heal(self,healingPower):
        self.player.heal(healingPower)

    def launchGrenade(self, direction,grenades_group):
        self.player.launchGrenade(direction,grenades_group)
    
    def getCurrentVelocity(self):
        return self.player.getCurrentVelocity()
    
    def setGrabbed(self, dy,barnacleRect):
        self.player.setGrabbed(dy,barnacleRect)

    def unSetGrabbed(self):
        self.player.unSetGrabbed()
    
    def setVolume(self, volume):
        super().setVolume(volume)
        self.shootEffect.set_volume(volume)

    def dash(self):        
            self.player.dash()

    def unDash(self):
        self.player.unDash()
      
    def lookUp(self):
      self.player.lookUp()

    def lookDown(self):
      self.player.lookDown()
      
    def shakeOn(self):
        self.player.shakeOn()

    def getDashCooldown(self):
        return self.player.getDashCooldown()
    def getHoldDash(self):
        return self.player.getHoldDash()
    def setHoldDash(self, b):
        self.player.setHoldDash(b)
    def setDashing(self, b):
        self.player.setDashing(b)
    def setDashDuration(self, n):
        self.player.setDashDuration(n)
    def setDashCooldown(self, n):
        self.player.setDashCooldown(n)
    
    def setHealth(self, n):
            self.player.setHealth(n)