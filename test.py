import random
import pygame as pg


pg.init()

BG_COLOR = pg.Color('gray12')
ENEMY_IMG = pg.Surface((50, 30))
ENEMY_IMG.fill(pg.Color('darkorange1'))
BULLET_IMG = pg.Surface((9, 15))
BULLET_IMG.fill(pg.Color('aquamarine2'))


class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=pos)
        self.health = 30

    def update(self, dt):
        if self.health <= 0:
            self.kill()


class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, -450)
        self.damage = 10

    def update(self, dt):
        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos  # Update the rect pos.
        if self.rect.bottom <= 0:
            self.kill()


class Game:

    def __init__(self):
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))

        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        for i in range(15):
            pos = (random.randrange(30, 750), random.randrange(500))
            Enemy(pos, self.all_sprites, self.enemies)

        self.bullet_timer = .1
        self.done = False

    def run(self):
        while not self.done:
            # dt = time since last tick in milliseconds.
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.run_logic(dt)
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def run_logic(self, dt):
        mouse_pressed = pg.mouse.get_pressed()
        self.all_sprites.update(dt)

        self.bullet_timer -= dt  # Subtract the time since the last tick.
        if self.bullet_timer <= 0:
            self.bullet_timer = 0  # Bullet ready.
            if mouse_pressed[0]:  # Left mouse button.
                # Create a new bullet instance and add it to the groups.
                Bullet(pg.mouse.get_pos(), self.all_sprites, self.bullets)
                self.bullet_timer = .1  # Reset the timer.

        # hits is a dict. The enemies are the keys and bullets the values.
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.health -= bullet.damage

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    Game().run()
    pg.quit()