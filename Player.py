import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images, dead_image, jump_fx=None, game_over_fx=None):
        super().__init__()
        self.images_right, self.images_left = images
        self.dead_image = dead_image
        self.jump_fx = jump_fx
        self.game_over_fx = game_over_fx
        self.reset(x, y)

    def update(self, game_over, world, blob_group, lava_group, exit_group, platform_group, screen):
        if game_over == 0:
            self.handle_input()
            self.handle_animation()
            self.apply_gravity()
            game_over = self.check_collisions(world, blob_group, lava_group, exit_group, platform_group)
            self.update_position()
        elif game_over == -1:
            self.handle_game_over()
        
        self.draw(screen)
        return game_over

    def handle_input(self):
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
            self.jump()
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            self.update_image()
        
        self.dx = dx

    def jump(self):
        if self.jump_fx:
            self.jump_fx.play()
        self.vel_y = -15
        self.jumped = True

    def handle_animation(self):
        walk_cooldown = 5
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images_right)
            self.update_image()

    def update_image(self):
        if self.direction == 1:
            self.image = self.images_right[self.index]
        elif self.direction == -1:
            self.image = self.images_left[self.index]

    def apply_gravity(self):
        self.vel_y = min(self.vel_y + 1, 10)
        self.dy = self.vel_y

    def check_collisions(self, world, blob_group, lava_group, exit_group, platform_group):
        self.in_air = True
        game_over = self.check_enemy_collisions(blob_group) or \
                    self.check_lava_collisions(lava_group) or \
                    self.check_exit_collisions(exit_group)

        self.check_tile_collisions(world)
        self.check_platform_collisions(platform_group)

        return game_over

    def check_tile_collisions(self, world):
        for tile in world.tile_list:
            self.handle_x_collision(tile)
            self.handle_y_collision(tile)

    def handle_x_collision(self, tile):
        if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
            self.dx = 0

    def handle_y_collision(self, tile):
        if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
            if self.vel_y < 0:  # Jumping
                self.dy = tile[1].bottom - self.rect.top
                self.vel_y = 0
            elif self.vel_y >= 0:  # Falling
                self.dy = tile[1].top - self.rect.bottom
                self.vel_y = 0
                self.in_air = False

    def check_enemy_collisions(self, blob_group):
        if pygame.sprite.spritecollide(self, blob_group, False):
            if self.game_over_fx:
                self.game_over_fx.play()
            return -1

    def check_lava_collisions(self, lava_group):
        if pygame.sprite.spritecollide(self, lava_group, False):
            if self.game_over_fx:
                self.game_over_fx.play()
            return -1

    def check_exit_collisions(self, exit_group):
        if pygame.sprite.spritecollide(self, exit_group, False):
            return 1

    def check_platform_collisions(self, platform_group):
        col_thresh = 20
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                self.handle_platform_collision(platform, col_thresh)

    def handle_platform_collision(self, platform, col_thresh):
        if abs((self.rect.top + self.dy) - platform.rect.bottom) < col_thresh:
            self.vel_y = 0
            self.dy = platform.rect.bottom - self.rect.top
        elif abs((self.rect.bottom + self.dy) - platform.rect.top) < col_thresh:
            self.rect.bottom = platform.rect.top - 1
            self.in_air = False
            self.dy = 0
        if platform.move_x != 0:
            self.rect.x += platform.move_direction

    def update_position(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def handle_game_over(self):
        self.image = self.dead_image
        print("Game Over!!")
        if self.rect.y > 200:
            self.rect.y -= 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self, x, y):
        self.index = 0
        self.counter = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.dx = 0
        self.dy = 0

# Helper function to load images
def load_player_images():
    images_right = []
    images_left = []
    for num in range(1, 5):
        img_right = pygame.image.load(f'img/guy{num}.png')
        img_right = pygame.transform.scale(img_right, (40, 80))
        img_left = pygame.transform.flip(img_right, True, False)
        images_right.append(img_right)
        images_left.append(img_left)
    dead_image = pygame.image.load('img/ghost.png')
    return images_right, images_left, dead_image