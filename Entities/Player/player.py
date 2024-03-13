import pygame
from .PlayerStates.idle import Idle
from .PlayerStates.run import Run
from .PlayerStates.jump import Jump
from math import floor
from Constants.constants import *
from MovementAndCollisions.movement import *
from .playerAbstract import PlayerAbstract
from Entities.shield import Shield
import random


class Player(PlayerAbstract):
        def __init__(self, x, y,uiHearts, uiText, dificulty):
            super().__init__(x, y, dificulty)
            self.dificulty = dificulty
            # Imagenes - patron estado
            self.states = {
                "IDLE": Idle(False),
                "RUN": Run(False),
                "JUMP": Jump(False)
            }
            """"RUN": Run(False),
                "JUMP": Jump(False)"""
            self.anim = 0
                # State para empezar
            self.state_name = "IDLE"
            self.state = self.states[self.state_name]

            self.standing = self.state.get_initial()
            self.deadImage = pygame.transform.rotate(self.standing,90)
            self.hitImage = pygame.transform.rotate(self.standing,90)
            self.shaking = -1
            self.currentVelocity = 0
            self.interactedOnce = False

            self.addObserver(uiText)
            self.addObserver(uiHearts)

            #Dash (luego se mueve)
            self.dashing = False
            self.dashCooldown = 0
            self.holdDash = False
            self.dashDuration = 0
            self.lookingUp = False
            self.lookingDown = False

        def changeStates(self):
            pass

        def change_state(self):
            self.state.done = False
            self.state_name = self.state.next_state
            left = self.state.left

            persistent = self.state.persist
            self.state = self.states[self.state_name]
            if left:
                self.state.left = True
            else:
                self.state.left = False
                # Por ahora esto esta vacio
            self.state.startup(persistent)
        
        # FUNCIONES MOVIMIENTO
        def idle(self):
            self.state.done = True
            self.state.next_state = self.state.posibleNexts["IDLE"]

        def move_left(self):
            self.moving_left = True
            self.state.done = True
            self.state.left = True
            self.state.next_state = self.state.posibleNexts["RUN"]

        def move_right(self):
            self.moving_right = True
            self.state.done = True
            self.state.left = False
            self.state.next_state = self.state.posibleNexts["RUN"]

        def jump(self):
            self.jumping = True
            if self.inAir:
                self.jumpEffect.stop()
                self.jumpEffect.play()
                self.state.done = True
                self.state.next_state = self.state.posibleNexts["JUMP"]

        def dash(self):
            if self.dashCooldown == 0 and self.holdDash == False:
                self.dashing = True
                self.dashDuration = 0
                self.dashCooldown = 100
                self.holdDash = True 

        def unDash(self):
            self.holdDash = False
        
        def lookUp(self):
            self.lookingUp = True

        def lookDown(self):
            self.lookingDown = True

        def getHp(self):
            return self.healthPoints
        
        def hit(self, damage):
            if self.hitCooldown < 0:
                self.standing = self.hitImage
                self.healthPoints -= damage
                self.hitCooldown = 60
                self.notify()
            return True

        def doInteract(self, interactuableGroup):
            interactsWith = pygame.sprite.spritecollideany(self, interactuableGroup)
            
            if interactsWith and not self.interactedOnce:
                self.interactedOnce = True
                interactsWith.interact()
                
        def interact(self, interactuableGroup):
            interactsWith = pygame.sprite.spritecollideany(self, interactuableGroup)
            if interactsWith:
                newText = interactsWith.getText()
                if newText != self.interactuableText:
                    self.interactuableText = newText
                    self.notify()
            elif self.interactuableText != "":
                self.interactuableText = ""
                self.notify()
        
        def interactTrigger(self, triggerGroup):
            interactsWith = pygame.sprite.spritecollideany(self, triggerGroup)
            if interactsWith:
                interactsWith.interact()
            
        def getInteractuableText(self):
            return self.interactuableText

        def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset) -> tuple:
            cameraOffsetX, cameraOffsetY = cameraOffset

            self.interact(interactuableGroup)
            self.interactTrigger(triggerGroup)
            self.hitCooldown -= 1

            print(self.currentVelocity)

            normalMovement = True
            
            if self.dashing:
                normalMovement = False
                if self.dashDuration == 0:
                    if self.moving_left and self.moving_right == False:
                        self.currentVelocity = -DASH_SPEED
                        self.left_mov = DASH_SPEED
                        self.dashDuration = 1
                    if self.moving_left == False and self.moving_right:
                        self.currentVelocity = DASH_SPEED
                        self.right_mov = DASH_SPEED
                        self.dashDuration = 1
                    if self.lookingUp and self.lookingDown == False:
                        self.velY = -DASH_SPEED
                        self.dashDuration = 1
                    if self.lookingUp == False and self.lookingDown:
                        self.velY = DASH_SPEED
                        self.dashDuration = 1
                    if self.dashDuration == 0:
                        #Cancelar el dash
                        self.dashCooldown = 0
                        normalMovement = True
                elif self.dashDuration > 0 and self.dashDuration <= DASH_DURATION:
                    self.dashDuration += 1
                else:
                    self.dashing = False
                    normalMovement = True


            if normalMovement:

                # Calculo del movimiento horizontal
                
                self.left_mov = move_horizontal(self.moving_left, self.left_mov, dt)
                self.right_mov = move_horizontal(self.moving_right, self.right_mov, dt)
                self.currentVelocity = self.right_mov - self.left_mov
            

                # Calculo del movimiento vertical
                if self.jumping and self.inAir == False and self.pressed_jump == 0:
                    self.velY = -MIN_JUMP_HEIGHT
                    self.hold_jump = True
                elif self.jumping == False or self.pressed_jump > MAX_JUMP_HEIGHT:
                    self.hold_jump = False
                elif self.jumping and self.inAir and self.hold_jump:
                    self.velY = -MIN_JUMP_HEIGHT
                    self.pressed_jump += 1

                # Para que al mantener el espacio solo salte una vez
                if self.jumping == False:
                    self.pressed_jump = 0

                # Se añade la gravedad al movimiento en y
                self.velY += (GRAVITY * dt//1000)
                if self.velY > MAX_FALL_VELOCITY:
                     self.velY = MAX_FALL_VELOCITY
            dy = self.velY
            dx = self.currentVelocity

            if self.dashCooldown > 0:
                self.dashCooldown -= 1

            self.inAir = True

            if self.grabbed:
                dx = 0
                dy = -self.dragSpeed

            # Se calculan las colisiones en ambos ejes
            tileHitBoxList = world.getTilesList()
            platformHitBoxList = world.getPlatformsList()
            destructibleHitBoxList = world.getDestructiblesList()

            auxRect = pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)
            auxRect2 = pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)
            
            tileIndex = auxRect.collidelist(tileHitBoxList)
            tileIndex2 = auxRect2.collidelist(tileHitBoxList)

            platformIndex = auxRect2.collidelist(platformHitBoxList)

            destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
            destructibleIndex2 = auxRect2.collidelist(destructibleHitBoxList)


            if tileIndex >= 0 or destructibleIndex >= 0:
                dx = 0
            
            if tileIndex2 >= 0:
                if self.velY < 0: #Saltando
                    dy = tileHitBoxList[tileIndex2].bottom - self.rect.top
                    self.pressed_jump = MAX_JUMP_HEIGHT +1
                    self.velY = 0
                elif self.velY >= 0: #Cayendo
                    dy = tileHitBoxList[tileIndex2].top - self.rect.bottom
                    self.velY = 0
                    self.inAir = False

            if destructibleIndex2 >= 0:
                if self.velY < 0: #Saltando
                    dy = destructibleHitBoxList[destructibleIndex2].bottom - self.rect.top
                    self.pressed_jump = MAX_JUMP_HEIGHT +1
                    self.velY = 0
                elif self.velY >= 0: #Cayendo
                    dy = destructibleHitBoxList[destructibleIndex2].top - self.rect.bottom
                    self.velY = 0
                    self.inAir = False

            if platformHitBoxList[platformIndex].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformIndex].top) < 15: #Cayendo
                        dy = - (self.rect.bottom - platformHitBoxList[platformIndex].top)
                        self.velY = 0
                        self.inAir = False
                        """ self.state.done = True
                        self.state.next_state = self.state.posibleNexts["STOP-JUMP"]"""
            
            cameraOffsetX = 0
            cameraOffsetY = 0


            # Si el jugador se mueve en los limites del scroll se mueve sin mas, si no se hace scroll
            if self.rect.x > SCREEN_WIDTH / 3 and self.rect.x < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            elif self.rect.x + dx > SCREEN_WIDTH / 3 and self.rect.x + dx < SCREEN_WIDTH - (SCREEN_WIDTH / 3):
                self.rect.x += dx 
            else:
                cameraOffsetX = dx

            if self.rect.y > (SCREEN_HEIGTH / 2) and self.rect.y < SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            elif self.rect.y + dy >= (SCREEN_HEIGTH / 2) and self.rect.y + dy <= SCREEN_HEIGTH - (SCREEN_HEIGTH / 2):
                self.rect.y += dy
            else:
                cameraOffsetY = dy

            # Se reinician las variables de movimiento
            self.moving_left = False
            self.moving_right = False
            self.lookingUp = False
            self.lookingDown = False

            shakingX = 0
            shakingY = 0

            if self.jumping or self.shaking:
                self.shaking = 30

            if self.shaking:
                self.shaking -= 1
                
                #shakingX = random.randint(0, 8) - 4
                #shakingY = random.randint(0,8) - 4

            self.jumping = False

            if self.state.done:
                self.change_state()

            self.interact(interactuableGroup)
            self.hitCooldown -= 1

            if self.anim > 6:
                self.standing = self.state.next_sprite(self.direction)
                self.anim = 0
            self.anim += 1
            
            return (cameraOffsetX + shakingX, cameraOffsetY + shakingY)

        def shoot(self, direction, bulletsGroup):
            print("No tengo arma")

        def draw(self, screen):
            offsetX = self.rect.x - 23
            screen.blit(self.standing, (offsetX, self.rect.y, self.rect.width, self.rect.height))
            #pygame.draw.rect(screen, (255,255,255), self.rect)
   

        def addObserver(self, observer):
            self.uiElementsList.append(observer)
    
        def delObserver(self, observer):
            self.uiElementsList.remove(observer)

        def notify(self):
            for observer in self.uiElementsList:
                observer.update(self)

        def position(self):
            return self.rect
        
        def cover(self):
            print("No tengo escudo.")
        
        def deflect(self, direction, bulletImage, velocidadBala):
            print("No se puede dar este caso")

        def heal(self, healingPower):
            self.healthPoints += healingPower
            if self.healthPoints >= self.maxHealthPoints:
                self.healthPoints = self.maxHealthPoints
            self.notify()
        
        def shootUpdateSprites(self, direction):
            pass
            
        def launchGrenade(self, direction,grenades_group):
            print("No tengo lanza grandas")
                
        def getCurrentVelocity(self):
            return self.currentVelocity
        
        def getShieldHp(self):
            return 0

        def setGrabbed(self, dy, barnacleRect):
            self.grabbed = True
            self.dragSpeed = dy
            self.rect.x = barnacleRect.x

        def unSetGrabbed(self):
            self.grabbed = False
            self.dragSpeed = 0
        
                

            