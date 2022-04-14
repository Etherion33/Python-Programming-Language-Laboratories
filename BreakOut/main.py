# arkanoid
import pygame
from pygame import gfxdraw
from pygame.locals import *
import os
from random import choice, randrange,randint

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        pygame.sprite.RenderPlain(self)

        self.velocity = [randint(2,4),randint(-4,4)]
        self.rect = self.image.get_rect()
        
    def update(self,dt):
        self.rect.x += self.velocity[0]#*dt
        self.rect.y += self.velocity[1]#*dt

    def draw(self, screen):
        pygame.draw.rect(self.image, self.color, [0,0,self.width, self.height])

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-4,4)
 
class Brick(pygame.sprite.Sprite):
    "One brick class"
 
    def __init__(self, color, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(self.image, self.color, [0,0, self.width,self.height])

        self.rect = self.image.get_rect()
        
    def update(self,dt):
        pass


    def draw(self,screen):
        pygame.draw.rect(self.image, self.color, [0,0, self.width, self.height])
 
 
class Bar(pygame.sprite.Sprite):
    "This is the bar class"
 
    def __init__(self, image): #color, width, height):
        super().__init__()
        self.color = RED

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        pygame.sprite.RenderPlain(self)
        
        self.rect = self.image.get_rect()
        self.rect.h 

    def update(self,dt):
        pass

    def draw(self,screen):
        pass


class Scene(object):
    def __init__(self):
        pass

    def render(self, screen,deltaTime):
        raise NotImplementedError

    def update(self, deltaTime):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class TitleScene(object):

    def __init__(self,game):
        super(TitleScene, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        self.game = game
        pygame.mixer.Sound.play(self.game.s_titlescreen)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('Arkanoid Game', True, (0, 200, 0))
        text2 = self.sfont.render('> press space to start <', True, (0, 200, 0))
        text3 = self.sfont.render('press escape to quit', True, (0, 200, 0))
        text4 = self.sfont.render('use mouse to move paddle', True, (0, 200, 0))
        screen.blit(text1, (screen.get_width()/3, screen.get_height()/3-50))
        screen.blit(text2, (screen.get_width()/3, (screen.get_height()/3)+50))
        screen.blit(text3, (screen.get_width()/3, (screen.get_height()/3)+150))
        screen.blit(text4, (screen.get_width()/3, (screen.get_height()/3)+200))


    def update(self,dt):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == K_SPACE:
                    self.manager.go_to(GameScene(self.game))
                if e.key == K_ESCAPE:
                    self.game.isRunning = False
                    return

class GameOver(Scene):
    def __init__(self,game):
        super(GameOver, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        self.game = game
        if self.game.lives > 0:
            pygame.mixer.Sound.play(self.game.s_over)
        else:
            pygame.mixer.Sound.play(self.game.s_over)

        for i in range(self.game.lives):
            self.game.score += 5

    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.game.lives > 0:
            text1 = self.font.render('You win!', True, (0, 200, 0))
            text2 = self.sfont.render('> Your score is : {}'.format(self.game.score),  True, (0, 200, 0))
            text3 = self.sfont.render('> press escape to quit <', True, (0, 200, 0))
        else:
            text1 = self.font.render('You lose!', True, (0, 200, 0))
            text2 = self.sfont.render('> Your score is : {}'.format(self.game.score),  True, (0, 200, 0))
            text3 = self.sfont.render('> press escape to quit <', True, (0, 200, 0))

        screen.blit(text1, (screen.get_width()/3, screen.get_height()/3-50))
        screen.blit(text2, (screen.get_width()/3, (screen.get_height()/3)+50))
        screen.blit(text3, (screen.get_width()/3, (screen.get_height()/3)+150))

    def update(self, dt):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.isRunning = False
                    return

class GameScene(Scene):
    def __init__(self, game):
        super(GameScene, self).__init__()
        pygame.mixer.stop()
        pygame.mixer.Sound.play(game.s_game)

        DEFAULT_PADDLE = pygame.image.load(os.path.join('Paddles', 'DX_Board.png')).convert_alpha()
        BIG_PADDLE = pygame.image.load(os.path.join('Paddles', 'DX_Board_Big.png')).convert_alpha()
        CATCH_PADDLE = [pygame.image.load(os.path.join('Paddles', 'Dx_Board_Catch.png')).convert_alpha()
        ,pygame.image.load(os.path.join('Paddles', 'Dx_Board_Catch.png')).convert_alpha()
        ,pygame.image.load(os.path.join('Paddles', 'Dx_Board_Catch.png')).convert_alpha()
        ,pygame.image.load(os.path.join('Paddles', 'Dx_Board_Catch.png')).convert_alpha()]

        

        DEFAULT_BALL = pygame.image.load(os.path.join('Balls', 'Ball.png')).convert_alpha()
        RED_BALL = pygame.image.load(os.path.join('Balls', 'Ball.png')).convert_alpha()

 
        self.game = game
        self.game.lives = 3
        self.game.score = 0
        self.stage = 0

        self.sprite_list = pygame.sprite.Group()

        #Create the Paddle
        self.bar = Bar(DEFAULT_PADDLE)
        self.bar.rect.x = 120
        self.bar.rect.y = 700

        #Create the ball sprite
        self.ball = Ball(DEFAULT_BALL)
        self.ball.rect.x = 300
        self.ball.rect.y = 400


        self.blist = pygame.sprite.Group()
        offset = 0
        for i in range(5):
            for j in range(9):
                randomcolor = randrange(0,255), randrange(0,255), randrange(0,255)
                brick = Brick(randomcolor,80,30)
                brick.rect.x = 100 + j * 90
                brick.rect.y = 80 + offset
                self.blist.add(brick)
                self.sprite_list.add(brick)
            offset += 40 
        
        print(len(self.blist))
        print(len(self.sprite_list))

        self.paddlelist = pygame.sprite.Group()
        self.paddlelist.add(self.bar)

        self.sprite_list.add(self.bar)
        self.sprite_list.add(self.ball)
            
        self.playtime = 0.0
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 24)
        self.width = 0
        self.height = 0

        self.xBarPos = 0.0
        self.curMousePosX = 0.0
        self.curMousePosY = 0.0
        self.curBallPosX = 0.0
        self.curBallPosY = 0.0

        pygame.mouse.set_visible(False)
            
    def debug_screen(self,screen):
        debug_info = self.sfont.render("-----DEBUG MODE-----", True, (0, 200, 0))
        mouse_info = self.sfont.render("Mouse position : {} {}".format(self.curMousePosX, self.curMousePosY), True, (0, 200, 0))
        bar_info = self.sfont.render("Bar position : {} {}".format(self.xBarPos, self.curMousePosY), True, (0, 200, 0))
        ball_info = self.sfont.render("Ball position : {} {}".format(self.ball.rect.x, self.ball.rect.y), True, (0, 200, 0))
        velocity_info = self.sfont.render("Ball velocity : X {} Y {}".format(self.ball.velocity[0], self.ball.velocity[1]), True, (0, 200, 0))
        player_info = self.sfont.render("Lifes: {} Score: {}".format(self.game.lives, self.game.score), True, (0, 200, 0))
        stage_info  = self.sfont.render("Stage : {}".format(self.stage), True, (0, 200, 0))

        screen.blit(debug_info, (0, 0))
        screen.blit(mouse_info, (0, 20))
        screen.blit(bar_info, (0, 40))
        screen.blit(ball_info, (0, 60))
        screen.blit(velocity_info, (0, 80))
        screen.blit(player_info, (0, 100))
        screen.blit(stage_info, (0, 120))



    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.game.debug == 1:
            self.debug_screen(screen)
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.sprite_list.draw(screen)
        if self.game.debug == 0:
            player_info = self.sfont.render("Lifes: {} Score: {}".format(self.game.lives, self.game.score), True, (0, 200, 0))
            screen.blit(player_info, (0, 0))

    def update(self, dt):

        #Checking cursor position
        self.curMousePosX = pygame.mouse.get_pos()[0]
        self.curMousePosY = pygame.mouse.get_pos()[1]
        self.xBarPos = pygame.mouse.get_pos()[0]
        #Setting mouse position to paddle position
        pygame.mouse.set_pos(self.bar.rect.x, self.bar.rect.y)

        #Constrain the paddle movement
        if self.xBarPos > 10 and self.xBarPos < self.width - self.bar.width:
            self.bar.rect.x = self.xBarPos


        #Constrain the ball movement
        if self.ball.rect.x <= 0:
            self.ball.velocity[0] = -self.ball.velocity[0]# * dt
            if self.ball.rect.x < 10:
                print("Hit wall !")
        if self.ball.rect.y <= 0:
            self.ball.velocity[1] = -self.ball.velocity[1]# * dt
            if self.ball.rect.y < 10:
                print("Hit wall !")

        if self.ball.rect.x >= 1000:
            self.ball.velocity[0] = -self.ball.velocity[0]# * dt
            if self.ball.rect.x > 950:
                print("Hit wall !")
        if self.ball.rect.y >= 750:
            self.ball.velocity[1] = -self.ball.velocity[1]# * dt
            self.game.lives-=1
            if self.ball.rect.y > 758:
                print("Hit wall !")

        #Make sure the ball velocity is not 0 
        if(self.ball.velocity[1] == 0) :
            self.ball.velocity[1] = randint(-8,8)

        #Checking the collisions of ball with paddle
        paddle_collision_list = pygame.sprite.spritecollide(self.ball,self.paddlelist,False)
        for paddle in paddle_collision_list:
            print("Hit paddle!")
            self.ball.rect.x -= self.ball.velocity[0]
            self.ball.rect.y -= self.ball.velocity[1]
            self.ball.bounce()

        #Checking the collisions of ball with bricks
        brick_collision_list = pygame.sprite.spritecollide(self.ball,self.blist,False)
        for brick in brick_collision_list:
            pygame.mixer.Sound.play(self.game.s_hitBrick)
            self.ball.bounce()
            self.game.score += 1
            brick.kill()


    
        #If player lost all lifes or destroy all bricks go to game over screen
        if(self.game.lives == 0 or  len(self.blist) == 0):
            pygame.mixer.stop()
            self.manager.go_to(GameOver(self.game))


        self.sprite_list.update(dt)

        self.playtime += dt/ 1000.0

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.isRunning = False
                    return



class SceneMananger(object):
    def __init__(self,game):
        self.go_to(TitleScene(game))

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class Game(object):

    def __init__(self, width=1024, height=768, fps=300):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 512)
        pygame.mixer.set_num_channels(32)
        pygame.display.set_caption('Arkanoid Game - Python')

        self.s_titlescreen = pygame.mixer.Sound('Music\\MainMenu.mp3')
        self.s_over = pygame.mixer.Sound('Music\\GameOver.mp3')
        self.s_game = pygame.mixer.Sound('Music\\Game.mp3')
        self.s_hitBrick = pygame.mixer.Sound('Music\\Explosion.wav')

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width , self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20 , bold = True)
        self.game = self
        self.isRunning = True
        self.debug = 0


    def mainloop(self):


        manager = SceneMananger(self.game)
        
        while self.isRunning:
            dt = 0
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0

            if pygame.event.get(QUIT):
                self.isRunning = False
                return
                
            manager.scene.handle_events(pygame.event.get())
            manager.scene.update(dt)
            manager.scene.draw(self.screen)
            dt = self.clock.tick(self.fps)/1000.0
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__': 
   Game(1024,768).mainloop()