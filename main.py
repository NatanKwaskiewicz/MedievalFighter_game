import pygame
import buttons
from pygame import mixer
from fighter import Fighter
from random import randint

mixer.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Medieval Fighter")

game_paused = False

clock = pygame.time.Clock()
FPS = 30

banknotes = []

class Cash():
    def __init__(self):
        self.x_cord = randint(200,700)
        self.y_cord = randint(410,410)
        
        self.image = (pygame.image.load("assets/images/icons/medkit.png"))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

        self.hp = 10
        
    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        screen.blit(self.image,(self.x_cord, self.y_cord))

cash=Cash()

BLUE = (0,0,205)
RED = (255, 0, 0)
RED_2 = (192, 32, 32)
GREEN = (34,139,34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

size = (1000, 600)
black_image = pygame.Surface(size, pygame.SRCALPHA)
black_image.set_alpha(100)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 48
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [15, 3]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WARRIOR2_SIZE = 48
WARRIOR2_SCALE = 4
WARRIOR2_OFFSET = [15, 3]
WARRIOR2_DATA = [WARRIOR2_SIZE, WARRIOR2_SCALE, WARRIOR2_OFFSET]

pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
sword2_fx = pygame.mixer.Sound("assets/audio/sword2.wav")
sword2_fx.set_volume(0.5)
win_fx = pygame.mixer.Sound("assets/audio/win.wav")
win_fx.set_volume(0.2)
secret_fx = pygame.mixer.Sound("assets/audio/s2.mp3")
secret_fx.set_volume(1)
kit_fx = pygame.mixer.Sound("assets/audio/kit.mp3")
kit_fx.set_volume(0.5)
med_fx = pygame.mixer.Sound("assets/audio/med.mp3")
med_fx.set_volume(0.5)


bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()
bg1_image = pygame.image.load("assets/images/background/background1.png").convert_alpha()

warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
warrior2_sheet = pygame.image.load("assets/images/warrior2/Sprites/warrior2.png").convert_alpha()

resume_img = pygame.image.load("assets/images/icons/button_resume.png").convert_alpha()
quit_img = pygame.image.load("assets/images/icons/button_quit.png").convert_alpha()
start_img = pygame.image.load("assets/images/icons/button_start.png").convert_alpha()
bt_medkit_img = pygame.image.load("assets/images/icons/button_medkit.png").convert_alpha()
secret_img = pygame.image.load("assets/images/icons/secret.png").convert_alpha()

resume_button = buttons.Button(420,150, resume_img,1)
quit_button = buttons.Button(450,250, quit_img,1)
quit2_button = buttons.Button(450,400, quit_img,1)
start_button = buttons.Button(320,200, start_img,1)
medkit_button = buttons.Button(320,300, bt_medkit_img,1)

WARRIOR_ANIMATION_STEPS = [8, 8, 1, 8, 8, 2, 8]
WARRIOR2_ANIMATION_STEPS = [8, 8, 1, 8, 8, 2, 8]

count_font = pygame.font.Font("assets/fonts/RoadPixel.ttf", 80)
score_font = pygame.font.Font("assets/fonts/RoadPixel.ttf", 30)
win_font = pygame.font.Font("assets/fonts/RoadPixel.ttf", 100)
P1 = win_font.render('PLAYER 1 WINS', True, BLUE)
P2 = win_font.render('PLAYER 2 WINS', True, RED_2)

start_txt = win_font.render('MEDIEVAL FIGHTER', True, WHITE)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))
def draw_bg1():
  scaled_bg = pygame.transform.scale(bg1_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, sword2_fx)
fighter_2 = Fighter(2, 700, 310, True, WARRIOR2_DATA, warrior2_sheet, WARRIOR2_ANIMATION_STEPS, sword_fx, sword2_fx)

secret = False
Medkit = False
start = True

run = True
spawn = 0 
while run:


  spawn += pygame.time.Clock().tick(30)/1000
  clock.tick(FPS)
  
  if start == True:
      draw_bg1()
      s = pygame.Surface((1000,600), pygame.SRCALPHA) 
      s.fill((0,0,0,200))                        
      screen.blit(s, (0,0))
      screen.blit(start_txt,(100, 60))
      if start_button.draw(screen):
          start = False
      if quit2_button.draw(screen):
          run = False
      if medkit_button.draw(screen):
          Medkit = True
          start = False
  else:
      draw_bg()
      
      draw_health_bar(fighter_1.health, 20, 20)
      draw_health_bar(fighter_2.health, 580, 20)
      draw_text("P1: " + str(score[0]), score_font, BLUE, 20, 60)
      draw_text("P2: " + str(score[1]), score_font, RED_2, 580, 60)

      if game_paused == False:
        if intro_count <= 0:
          fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
          fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
          draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
          if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            
        if Medkit == True:     
            if spawn >= 6:
                spawn = 0
                banknotes.append(Cash())
            for banknote in banknotes:
                banknote.tick()
            for banknote in banknotes:
                if spawn >= 1:
                    if fighter_1.hitbox.colliderect(banknote.hitbox):
                        banknotes.remove(banknote)
                        if fighter_1.health == 100:
                            med_fx.play()
                        if fighter_1.health <= 90:
                            kit_fx.play()
                            fighter_1.health = fighter_1.health + 10
                    if fighter_2.hitbox.colliderect(banknote.hitbox):
                        banknotes.remove(banknote)
                        if fighter_2.health == 100:
                            med_fx.play()
                        if fighter_2.health <= 90:
                            kit_fx.play()
                            fighter_2.health = fighter_2.health + 10

        fighter_1.update()
        fighter_2.update()

      fighter_1.draw(screen)
      fighter_2.draw(screen)
  
  
  for banknote in banknotes:
      banknote.draw()

  if round_over == False:
    if fighter_1.alive == False:
      if (score[0] == 5 and score[1] == 9):
        secret_fx.play()
        secret = True
      else:
        win_fx.play()
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    if fighter_2.alive == False:
      if (score[0] == 5 and score[1] == 9):
        secret_fx.play()
        secret = True
      else:
        win_fx.play()
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
      
  if fighter_1.alive == False or fighter_2.alive == False:
    if secret == True:
      screen.blit(secret_img, (280, 100))
    else:
        secret = False
        if fighter_1.alive == True:
            screen.blit(P1,(180, 120))
        if fighter_2.alive == True:
            screen.blit(P2,(180, 120))
        
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      secret = False
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, sword2_fx)
      fighter_2 = Fighter(2, 700, 310, True, WARRIOR2_DATA, warrior2_sheet, WARRIOR2_ANIMATION_STEPS, sword_fx, sword2_fx)

  if game_paused == True:
    s = pygame.Surface((1000,600), pygame.SRCALPHA) 
    s.fill((0,0,0,200))                        
    screen.blit(s, (0,0))
    if resume_button.draw(screen):
      game_paused = False
    if quit_button.draw(screen):
      run = False
    
    
      
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()


pygame.quit()
