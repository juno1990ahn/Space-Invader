
import pygame
import threading
from constants import *
from observer import *

def load_image(name):
    return pygame.image.load(SPRITE_FOLDER + name).convert_alpha()

def load_sound(name):
    return pygame.mixer.Sound(AUDIO_FOLDER + name)

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Entity, self).__init__()
        self.sprites = []
        self.rect = pygame.Rect(x, y, w, h)
        self.image = None
        self.x_vel = 0
        self.y_vel = 0
        self.sprite_index = 0

class Player(Entity, Observer):
    def __init__(self, x, y, playable_area):
        Entity.__init__(self, x, y, 26, 16)
        Observer.__init__(self)
        self.playable_area = playable_area.inflate(playable_area.width * -.05, 0)
        self.sprites.append(load_image('player.png'))
        self.image = self.sprites[self.sprite_index]
        self.last_key = None
        self.can_shoot = True
        # self.shoot_sound = load_sound('shoot.mp3')
        # self.death_sound = load_sound('explosion.wav')

    def onEvent(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.last_key = event.key
                self.x_vel = -5
            elif event.key == pygame.K_RIGHT:
                self.last_key = event.key
                self.x_vel = 5
            elif event.key == pygame.K_SPACE:
                if self.can_shoot:
                    self.can_shoot = False
                    bullet = Bullet(self.rect.centerx, self.rect.centery, True)
                    game.player_bullets.add(bullet)
                    # self.shoot_sound.play()
                    threading.Timer(0.5, self.allow_shoot).start()

        elif event.type == pygame.KEYUP:
            if self.last_key != None and event.key == self.last_key:
                self.x_vel = 0
                self.last_key = None

    def allow_shoot(self):
        self.can_shoot = True

    def update(self):
        Entity.update(self)
        self.rect.move_ip(self.x_vel, self.y_vel)
        self.rect.clamp_ip(self.playable_area)

    def kill(self):
        # self.death_sound.play()
        Entity.kill(self)

class DeadPlayer(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x - 2, y, 30, 16)
        self.image = load_image('dead_player.png')
        self.death_timer = threading.Timer(1.0, self.kill)
        self.death_timer.start()
        
class Invader(Entity):
    def __init__(self, x, y, type):
        if (type == 0):
            Entity.__init__(self, x + 4, y, 16, 16)
            self.sprites.append(load_image('invader_1_1.png'))
            self.sprites.append(load_image('invader_1_2.png'))
        elif (type == 1):
            Entity.__init__(self, x + 1, y, 22, 16)
            self.sprites.append(load_image('invader_2_1.png'))
            self.sprites.append(load_image('invader_2_2.png'))
        elif (type == 2):
            Entity.__init__(self, x, y, 24, 16)
            self.sprites.append(load_image('invader_3_1.png'))
            self.sprites.append(load_image('invader_3_2.png'))
        self.image = self.sprites[self.sprite_index]
        self.animation_speed = 20
        self.current_animation_cnt = self.animation_speed
        self.x_vel = 3
        self.y_vel = 0
        self.x_steps = 25
        self.current_x_step = self.x_steps
        # self.shoot_sound = load_sound('invader_shoot.mp3')
        # self.death_sound = load_sound('invaderkilled.wav')

    def update(self):
        if self.current_animation_cnt == 0:
            # update sprite animation
            self.sprite_index = self.sprite_index + 1
            if self.sprite_index == len(self.sprites):
                self.sprite_index = 0
            self.image = self.sprites[self.sprite_index]

            # update position
            if self.current_x_step == 0:
                prev_x = self.x_vel
                self.x_vel = 0
                self.y_vel = 10
                self.current_x_step = self.x_steps
                self.rect.move_ip(self.x_vel, self.y_vel)
                self.x_vel = prev_x * -1
                self.y_vel = 0
                self.animation_speed = self.animation_speed - 2
                if self.animation_speed <= 0:
                    self.animation_speed = 1
            else:
                self.current_x_step = self.current_x_step - 1
                self.rect.move_ip(self.x_vel, self.y_vel)

            self.current_animation_cnt = self.animation_speed
        else:
            self.current_animation_cnt = self.current_animation_cnt - 1

    def shoot(self, game):
        # self.shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.centery, False)
        game.enemy_bullets.add(bullet)


    def kill(self):
        # self.death_sound.play()
        Entity.kill(self)


class DeadInvader(Entity):
    def __init__(self, centerx, centery):
        Entity.__init__(self, centerx - 13, centery - 8 , 26, 16)
        self.image = load_image('dead_invader.png')
        self.death_timer = threading.Timer(0.3, self.kill)
        self.death_timer.start()

class Bullet(Entity):
    def __init__(self, x, y, flip):
        Entity.__init__(self, x, y, 6, 12)
        self.vel = -5 if flip else 5
        angle = 180 if flip else 0
        self.image = pygame.transform.rotate(load_image('bullet.png'), angle)

    def update(self):
        self.rect.move_ip(0, self.vel)

class HUD:
    def __init__(self):
        self.hud_font = pygame.font.SysFont(HUD_FONT_TYPE, HUD_FONT_SIZE)
        self.score_text = 'SCORE: '
        self.lives_text = 'LIVES LEFT: '
        self.game_over_text = 'GAME OVER'
        self.you_won_text = 'YOU WON'
        self.game_over = self.hud_font.render(self.game_over_text, 1, WHITE)
        self.you_won = self.hud_font.render(self.you_won_text, 1, WHITE)

    def draw(self, screen, state):
        self.hi_score = self.hud_font.render(self.score_text + str(state.score), 1, WHITE)
        self.lives = self.hud_font.render(self.lives_text + str(state.lives), 1, WHITE)
        screen.blit(self.hi_score, (STARTING_POSITIONS['HI_SCORE']['x'], STARTING_POSITIONS['HI_SCORE']['y']))
        screen.blit(self.lives, (STARTING_POSITIONS['LIVES']['x'], STARTING_POSITIONS['LIVES']['y']))
        if state.isGameOver:
            centerx = screen.get_width() / 2
            centery = screen.get_height() / 2 
            if state.lives == 0:
                screen.blit(self.game_over, (centerx - self.game_over.get_width() / 2, centery - self.game_over.get_height() / 2))
            else:
                screen.blit(self.you_won, (centerx - self.you_won.get_width() / 2, centery - self.you_won.get_height() / 2))
