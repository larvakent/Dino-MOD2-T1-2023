import pygame 

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, SCORE_SOUND, BG_FUNDO_NOITE, BG_FUNDO_DIA, GAME_OVER, ICON_START
from dino_runner.components.dinosaur import Dinosaur 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager 
from dino_runner.utils.text_utils import draw_message_component 
from dino_runner.components.powerups.power_up_manager import PowerUpManager 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.time_to_blit = None
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.background = BG_FUNDO_DIA
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.score % 100 == 0:
                SCORE_SOUND.play()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    
    def draw_background(self):
        image_width = self.background.get_width()
        self.screen.blit(self.background, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(self.background, (image_width + self.x_pos_bg, self.y_pos_bg)) 
        if self.x_pos_bg <= -image_width:
            self.screen.blit(self.background, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= 2

        if self.score % 500 == 0:
            self.time_to_blit = pygame.time.get_ticks() + 7000
        if self.time_to_blit:
            self.background = BG_FUNDO_NOITE
            image_width = self.background.get_width()
            self.screen.blit(self.background, (self.x_pos_bg, self.y_pos_bg))
            self.screen.blit(self.background, (image_width + self.x_pos_bg, self.y_pos_bg)) 
            if self.x_pos_bg <= -image_width:
                self.screen.blit(self.background, (image_width + self.x_pos_bg, self.y_pos_bg))
                self.x_pos_bg = 0
            self.x_pos_bg -= 2
            if pygame.time.get_ticks() >= self.time_to_blit:
                self.time_to_blit = None
                self.background = BG_FUNDO_DIA
        

    def draw_score(self):
        draw_message_component(
            f"score: {self.score}",
            self.screen, 
            pos_x_center=1000,
            pos_y_center=50
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} enable for {time_to_show} seconds",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.blit(self.background, (0,0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON_START, (half_screen_width-50, half_screen_height-120))
            draw_message_component("Press any key to start", self.screen)
        else:
            self.screen.blit(GAME_OVER, (half_screen_width-190, half_screen_height-200))
            draw_message_component("Press any key to restart", self.screen, pos_y_center=half_screen_height + 140)
            draw_message_component(
                f"Your score: {self.score}", self.screen,
                pos_y_center=half_screen_height - 150
            )
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

        pygame.display.flip()

        self.handle_events_on_menu()

    

