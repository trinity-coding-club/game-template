import pygame

class Player(pygame.sprite.Sprite):
    
    # Constructor
    def __init__(self, x, y, jump_fx=None, game_over_fx=None):
        super().__init__()
        self.images_right, self.images_left, self.dead_image = self.load_player_images()
        self.jump_fx = jump_fx
        self.game_over_fx = game_over_fx
        self.score = 0
        self.health = 100
        self.last_enemy_collision_time = 0  # Time of last enemy/lava collision
        self.enemy_collision_delay = 1000  # 1 second delay for enemy collisions
        self.reset(x, y)

    
    # Runs in main game loop
    def update(self, game_over, screen, world):
        if not game_over:
            self.handle_input()
            self.handle_animation()
            self.apply_gravity()
            game_over = self.check_collisions(world)
            self.update_position()
        else:
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

    def check_collisions(self, world):
        self.in_air = True

        # Check for tile and platform collisions (no delay here)
        self.check_tile_collisions(world)
        self.check_platform_collisions(world.get_platform_group())

        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check enemy or lava collisions (with delay)
        if current_time - self.last_enemy_collision_time >= self.enemy_collision_delay:
            if self.check_enemy_collisions(world.enemy_group) or self.check_enemy_collisions(world.lava_group):
                self.health -= 20  # Take damage on enemy collision
                self.last_enemy_collision_time = current_time  # Update last enemy collision time
                if self.health <= 0:
                    return True  # Game over (health is zero or less)
                
        self.check_coin_collisions(world.coin_group)

        # Handle exit collision (no delay needed here)
        if self.check_exit_collisions(world.exit_group):
            self.score += 100  # Award score for level completion
            #TODO:Move to new level
            return 'level_completed' # Level completed, but not a game over

        return False

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

    def check_enemy_collisions(self, enemy):
        if pygame.sprite.spritecollide(self, enemy, False):
            if self.game_over_fx:
                self.game_over_fx.play()
            return True

    def check_exit_collisions(self, exit_group):
        if pygame.sprite.spritecollide(self, exit_group, False):
            return True
        
    def check_coin_collisions(self, coin_group):
        coins_collected = pygame.sprite.spritecollide(self, coin_group, True)  # True removes the coins
        if coins_collected:
            self.score += 10  # Increase score for each coin collected
            return True
        return False

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
        # print("Draw")
        screen.blit(self.image, self.rect)
    # Resets all important player variables
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

    # Static because doesn't need to access any player instances
    @staticmethod
    def load_player_images():
        images_right = []
        images_left = []
        for num in range(1, 5):
            img_right = pygame.image.load(f'media/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            images_right.append(img_right)
            images_left.append(img_left)
        dead_image = pygame.image.load('media/ghost.png')
        return images_right, images_left, dead_image
