
 
import pygame
import random
from constants import *
from entities import *
from observer import *

class GameState:
    def __init__(self):
        self.lives = LIVES
        self.isGameOver = False
        self.score = 0

class GameManager:
    def __init__(self, w, h):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.state = GameState()
        self.screen = pygame.display.set_mode((w, h))
        self.done = False
        self.keyStream = KeyboardStream()
        self.clock = pygame.time.Clock()
        self.initialize_entities()
        self.can_shoot = True

    def initialize_entities(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.dead_entities = pygame.sprite.Group()
        self.initialize_player()
        for row in range(ENEMY_GRID['y']):
            for col in range(ENEMY_GRID['x']):
                invader_type = (row + 1) // 2
                invader_x = screen_w * STARTING_POSITIONS['ENEMY']['x'] + col * screen_w * STARTING_POSITIONS['ENEMY']['SPACING']['x']
                invader_y = screen_h * STARTING_POSITIONS['ENEMY']['y'] + row * screen_h * STARTING_POSITIONS['ENEMY']['SPACING']['y']
                self.enemies.add(Invader(invader_x, invader_y, invader_type))
        self.hud = HUD()

    def initialize_player(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        self.player.add(Player(screen_w * STARTING_POSITIONS['PLAYER']['x'], screen_h * STARTING_POSITIONS['PLAYER']['y'], self.screen.get_rect()))
        self.keyStream.subscribe(self.player.sprite)

    def allow_shoot(self):
        self.can_shoot = True

    def update(self):

        if self.player.sprite == None:
            self.initialize_player()

        # Check collisions
        hit_player = pygame.sprite.spritecollide(self.player.sprite, self.enemies, False)
        if len(hit_player) > 0:
            self.state.isGameOver = True
            self.state.lives = 0
        else:
            hit_bullets = pygame.sprite.spritecollide(self.player.sprite, self.enemy_bullets, True)
            if len(hit_bullets) > 0:
                player_loc = self.player.sprite.rect
                self.keyStream.clear()
                self.player.add(DeadPlayer(player_loc.x, player_loc.y))
                self.state.lives -= 1
                self.state.isGameOver = self.state.lives == 0 

            hit_enemies = pygame.sprite.groupcollide(self.enemies, self.player_bullets, True, True)
            for enemy, bullet in hit_enemies.iteritems():
                self.dead_entities.add(DeadInvader(enemy.rect.centerx, enemy.rect.centery))
                self.state.score += 100
                self.state.isGameOver = len(self.enemies) == 0
            if self.can_shoot and len(self.enemies) > 0:
                self.can_shoot = False
                rand_enemy = int(len(self.enemies) * random.random())
                self.enemies.sprites()[rand_enemy].shoot(self)
                threading.Timer(0.8, self.allow_shoot).start()

        if self.state.isGameOver:
            self.clear()

        self.player.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.dead_entities.update()

    def render(self):
        # Draw background
        self.screen.fill(BLACK)
        # Draw player and enemies
        self.player.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.dead_entities.draw(self.screen)

        # Draw HUD
        self.hud.draw(self.screen, self.state)
        pygame.display.flip()

    def init_game(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    break
                elif event.type == pygame.KEYDOWN and self.state.isGameOver:
                    self.state = GameState()
                    self.initialize_entities()
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.keyStream.notifySubscribers(event, self)

            self.update()
            self.render()

            self.clock.tick(FPS)
        pygame.quit()

    def clear(self):
        self.player.empty()
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.dead_entities.empty()
        self.keyStream.clear()
        self.can_shoot = True

if __name__ == "__main__": 
    random.seed()
    game = GameManager(GAME_SIZE['w'], GAME_SIZE['h'])
    game.init_game()
