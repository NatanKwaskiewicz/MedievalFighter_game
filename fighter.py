import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, sound2):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.hitbox = pygame.Rect((x, y, 60, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = sound
    self.attack_sound2 = sound2
    self.hit = False
    self.health = 100
    self.alive = True

  def load_images(self, sprite_sheet, animation_steps):
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    key = pygame.key.get_pressed()

    if self.attacking == False and self.alive == True and round_over == False:
      if self.player == 1:
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        
        if key[pygame.K_r]:
          self.attack_type = 1
          self.attack(target)
        if key[pygame.K_t]:
          self.attack_type = 2
          self.attack(target)


      if self.player == 2:
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True

        if key[pygame.K_k]:
          self.attack_type = 1
          self.attack(target)
        if key[pygame.K_l]:
          self.attack_type = 2
          self.attack(target)


    self.vel_y += GRAVITY
    dy += self.vel_y

    if self.hitbox.left + dx < 0:
      dx = -self.hitbox.left
    if self.hitbox.right + dx > screen_width:
      dx = screen_width - self.hitbox.right
    if self.hitbox.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.hitbox.bottom

    if target.hitbox.centerx > self.hitbox.centerx:
      self.flip = False
    else:
      self.flip = True

    if self.attack_type  > 0:
      self.attack_cooldown -= 1

    self.hitbox.x += dx
    self.hitbox.y += dy



  def update(self):
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    self.image = self.animation_list[self.action][self.frame_index]
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    if self.frame_index >= len(self.animation_list[self.action]):
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        if self.action == 3:
          self.attacking = False
          self.attack_cooldown = 10
        if self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        if self.action == 5:
          self.hit = False
          self.attacking = False
          self.attack_cooldown = 10

  def attack(self, target):
    if self.attack_cooldown == 0:
      self.attacking = True
      if self.attack_type == 1:
        self.attack_sound.play()
        attacking_rect = pygame.Rect(self.hitbox.centerx - (2 * self.hitbox.width * self.flip), self.hitbox.y, 2 * self.hitbox.width, self.hitbox.height)
        if attacking_rect.colliderect(target.hitbox):
          target.health -= 10
          target.hit = True
      if self.attack_type == 2:
        self.attack_sound2.play()
        attacking_rect = pygame.Rect(self.hitbox.centerx - (2 * self.hitbox.width * self.flip), self.hitbox.y, 2 * self.hitbox.width, self.hitbox.height)
        if attacking_rect.colliderect(target.hitbox):
          target.health -= 20
          target.hit = True


  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.hitbox.x - (self.offset[0] * self.image_scale), self.hitbox.y - (self.offset[1] * self.image_scale)))
