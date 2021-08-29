# random for random numbers, math for some math functions, pygame where game is done, pickle for loading scores
import random
import math
import pygame
import pickle

# needs to be set for pygame functions to work
pygame.init()
pygame.font.init()

# where in the computer can the font type file be found
font_path = "/Users/aibek/Desktop/PressStart2P.ttf"

# this variables below are stored because they are referred to many times throughout the code
mainfont = pygame.font.Font(font_path, 60)
subfont = pygame.font.Font(font_path, 35)
smallfont = pygame.font.Font(font_path, 20)
boxfont = pygame.font.Font(font_path, 25)
escfont = pygame.font.Font(font_path, 18)
menufont = pygame.font.Font(font_path, 30)
tinyfont = pygame.font.Font(font_path, 11)

white = (255, 255, 255)
black = (0, 0, 0)
gold = (255, 215, 0)

purple = (168, 0, 255)
blue = (0, 121, 255)
green = (0, 241, 29)
yellow = (255, 239, 0)
orange = (255, 127, 0)
red = (255, 0, 0)
light_blue = (0, 191, 255)
pink = (255, 0, 127)
dull_blue = (72, 109, 125)
dull_orange = (242, 138, 78)
dull_green = (143, 182, 65)
dull_yellow = (255, 219, 97)
dull_pink = (254, 140, 166)
dull_red = (245, 96, 82)


# this variables are stored because they need to not be affected by the constant run loop of the game
color1 = gold
color2 = white
color3 = white
color4 = white
color5 = white
color6 = white
color7 = white
color8 = white
color9 = white
color10 = white
color11 = white

primary_color = white
secondary_color = black
previous_s_color = black

is_play_screen = False
game_key = False
one_player = True
is_pause = False
is_setting = False
is_high_score = False
is_help = False
is_new_hs = False
is_spin = True

is_appear = True
is_hit_box = True
arcade_effect = False
change_length = True
normal_move_paddle = True

is_first = True
is_second = False

bot = 0
score_limit = 0
mode = 0
score_select = 0
prob = 0
slow = 0
spin = 0

# loads scores from the separate file
top_scores = pickle.load(open("top_scores.rtf", "rb"))


def draw_box(x, y, width, height, thick, color):
    # basic function to draw a box
    x2 = x + width
    y2 = y + height
    pygame.draw.line(window, color, [x, y], [x2, y], thick)
    pygame.draw.line(window, color, [x, y2], [x2, y2], thick)
    pygame.draw.line(window, color, [x, y], [x, y2], thick)
    pygame.draw.line(window, color, [x2, y], [x2, y2], thick)


def render_text(text, font, color, x, y):
    # used to display text
    render = font.render(str(text), 1, color)
    window.blit(render, (x, y))


class GameWindow(object):
    def __init__(self, screen_height, screen_width, bound):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.bound = bound

    def draw_main_box(self):
        bound = self.bound
        screen_height = self.screen_height
        screen_width = self.screen_width
        shb = screen_height - bound
        swb = screen_width - bound

        # determined using trial and error
        draw_box(bound, bound, swb - bound - 1, shb - bound, 3, white)
        pygame.draw.line(window, white, [swb - bound * 3, bound], [swb - bound * 3, shb], 3)
        pygame.draw.line(window, white, [bound * 4, bound], [bound * 4, shb], 3)

    def draw_game_box(self):
        bound = self.bound
        screen_height = self.screen_height
        screen_width = self.screen_width
        shb = screen_height - bound
        swb = screen_width - bound

        draw_box(bound, bound, swb - bound - 1, shb - bound, 3, primary_color)
        pygame.draw.line(window, primary_color, [swb - bound * 3, bound], [swb - bound * 3, shb], 3)
        pygame.draw.line(window, primary_color, [bound * 4, bound], [bound * 4, shb], 3)

    def draw_mid(self):
        count = 0
        space = 20
        height = 20
        width = 4
        interval = height + space
        pos = [(self.screen_width - width) / 2, self.bound]
        while count < int(self.screen_height/interval):
            y = pos[1] + interval * count
            pygame.draw.line(window, primary_color, [pos[0], y], [pos[0], pos[1] + y + height], width)
            count += 1


class Paddles(object):
    def __init__(self, paddle_width, paddle_height, paddle_velocity):
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_velocity = paddle_velocity
        self.paddle1_pos = [self.paddle_width * 3, (game.screen_height - self.paddle_height)/2]
        self.paddle2_pos = [game.screen_width - self.paddle_width * 4, (game.screen_height - self.paddle_height)/2]

    def draw_paddles(self):
        # simply GUI
        window.fill(secondary_color)
        pygame.draw.rect(window, primary_color, (self.paddle1_pos[0], self.paddle1_pos[1], self.paddle_width, self.paddle_height))
        pygame.draw.rect(window, primary_color, (self.paddle2_pos[0], self.paddle2_pos[1], self.paddle_width, self.paddle_height))

    def player_move_paddle(self, up, down):
        # moves position of paddles depending whether the user pressed up or down keys
        if down and self.paddle1_pos[1] < game.screen_height - self.paddle_height - self.paddle_velocity:
            self.paddle1_pos[1] += self.paddle_velocity

        if up and self.paddle1_pos[1] > self.paddle_velocity:
            self.paddle1_pos[1] -= self.paddle_velocity

    def players_move_paddle(self, up, down):
        # same as above, but for the second user
        if down and self.paddle2_pos[1] < game.screen_height - self.paddle_height - self.paddle_velocity:
            self.paddle2_pos[1] += self.paddle_velocity

        if up and self.paddle2_pos[1] > self.paddle_velocity:
            self.paddle2_pos[1] -= self.paddle_velocity


class Ball(object):
    def __init__(self, ball_radius, ball_speed):
        self.ball_radius = ball_radius
        self.ball_pos = [int(game.screen_width / 2), int(game.screen_height / 2)]
        self.ball_speed = ball_speed

    def start_game(self):
        # this function contains the starting values so that when a player scores, those values reset
        # randoms whether the ball goes up or down, and right or left
        xstart = random.randint(1, 2)
        ystart = random.randint(1, 2)

        # the starting ball velocity
        self.ball_vel = [9, 5]

        # starting ball position, which is the middle of the screen
        self.ball_pos = [int(game.screen_width / 2), int(game.screen_height / 2)]

        # starting ball speed which would be altered through out the game
        self.ball_speed = 6

        # goes right or left and up or down depending on the above random variables
        if xstart == 1:
            self.ball_vel[0] = -self.ball_vel[0]
        if ystart == 1:
            self.ball_vel[1] = -self.ball_vel[1]

    def move_ball(self):
        pygame.draw.rect(window, primary_color, (self.ball_pos[0], self.ball_pos[1], self.ball_radius, self.ball_radius))

        # this gives the sheer direction of the ball
        unit_vel = ball.unit_vector(self.ball_vel[0], self.ball_vel[1])

        # this moves the ball; uses direction * the speed
        self.ball_pos[0] += int(unit_vel[0] * self.ball_speed)
        self.ball_pos[1] += int(unit_vel[1] * self.ball_speed)

    def wall_collision(self):
        if self.ball_pos[1] <= self.ball_radius or self.ball_pos[1] >= game.screen_height - self.ball_radius:
            self.ball_vel[1] = -self.ball_vel[1]

    def paddle_collision(self):
        ball_rect = (pygame.Rect(self.ball_pos[0], self.ball_pos[1], self.ball_radius, self.ball_radius))
        paddle1 = pygame.Rect(paddle.paddle1_pos[0], paddle.paddle1_pos[1], paddle.paddle_width, paddle.paddle_height)
        paddle2 = pygame.Rect(paddle.paddle2_pos[0], paddle.paddle2_pos[1], paddle.paddle_width, paddle.paddle_height)

        # 'colliderect' special pygame function that checks for rectangle collision.
        if paddle1.colliderect(ball_rect):
            # changes the x direction of the ball; makes right move to left
            self.ball_vel[0] = -self.ball_vel[0]
            # adds a slight speed increase to the ball
            self.ball_speed += 0.5

        if paddle2.colliderect(ball_rect):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_speed += 0.5

    @staticmethod
    def unit_vector(a, b):
        # based on mathematical formula
        # unit vector in math gives the sheer direction of a moving object
        v = [a, b]
        magnitude = (math.sqrt((v[0] ** 2) + (v[1] ** 2)))
        v[0] = v[0] / magnitude
        v[1] = v[1] / magnitude
        return v

    @staticmethod
    def dot_product(v1, v2, u1, u2):
        # based on mathematical formula
        dot = (v1 * u1) + (v2 * u2)
        return dot


class Score(object):
    def __init__(self, p1_score, p2_score):
        self.p1_score = p1_score
        self.p2_score = p2_score

    def score_collision(self):
        if ball.ball_pos[0] <= ball.ball_radius:
            self.p2_score += 1
            score.arcade_score()
            ball.start_game()
        elif ball.ball_pos[0] >= game.screen_width + ball.ball_radius:
            self.p1_score += 1
            score.arcade_score()
            ball.start_game()

    @staticmethod
    def arcade_score():
        global secondary_color
        if mode == 2:
            # if 'rainbow land' power up is active and player scores, the bg color should reset to previous
            if spin == 2:
                secondary_color = previous_s_color
            arcade.reset_arcade()

    def update_score(self):
        loc1 = 170
        loc2 = 120

        # this changes the location of the displayed score on the screen if it is a single or double digit num.
        if self.p1_score >= 10:
            loc1 = 200
        if self.p2_score >= 10:
            loc2 = 90

        label1 = mainfont.render(str(self.p1_score), 1, primary_color)
        window.blit(label1, (int(game.screen_width / 2)-loc1, int(game.screen_height / 12)))
        label2 = mainfont.render(str(self.p2_score), 1, primary_color)
        window.blit(label2, (int(game.screen_width / 2)+loc2, int(game.screen_height / 12)))


class AI(object):
    def __init__(self, prob, slow):
        self.prob = prob
        self.slow = slow

    def bot(self):
        prob = self.prob
        speed = ball.ball_speed - 2
        if pause():
            speed = 0

        # half the height of the paddle
        pmid = paddle.paddle_height/2

        # position of the second paddle; paddle of the bot
        pos = int(paddle.paddle2_pos[1])

        # velocity of the user paddle, which is 10
        vel = paddle.paddle_velocity

        # the original probability minus the speed of the ball; if ball gets faster, probability gets lower
        miss = int(prob - ball.ball_speed)

        # a random number from 1 to the original probability
        probability = random.randint(1, prob)

        # if random variable 'probability' is larger than the constant miss chance: speed of bot's paddle becomes slower
        if probability > miss:
            if self.slow < speed:
                speed = self.slow

        # makes sure that the speed of bot's paddle won't exceed maximum speed of user
        if speed > vel:
            speed = vel

        # checks whether the ball is moving right (towards the bot) or left (towards the human opponent)
        if ball.ball_vel[0] > 0:

            # collision theory
            if game.screen_height - paddle.paddle_height - vel - 2 > pos > vel + 2:
                if pos + 15 < int(ball.ball_pos[1]):
                    paddle.paddle2_pos[1] += speed
                if pos + paddle.paddle_height - 15 > int(ball.ball_pos[1]):
                    paddle.paddle2_pos[1] -= speed
            else:
                if pos < int(ball.ball_pos[1]):
                    paddle.paddle2_pos[1] += speed
                if pos + paddle.paddle_height > int(ball.ball_pos[1]):
                    paddle.paddle2_pos[1] -= speed
        else:

            # if the ball is moving the other direction, the bot will slowly move towards the middle
            if 0 < int(paddle.paddle2_pos[1] + pmid) < int(game.screen_height / 2 - 10):
                paddle.paddle2_pos[1] += speed / 2
            elif game.screen_height > int(paddle.paddle2_pos[1] + pmid) > int(game.screen_height / 2):
                paddle.paddle2_pos[1] -= speed / 2


def draw_main():

    # GUI drawings of the main menu; gives it the unique look.
    window.fill(black)
    GameWindow.draw_main_box(game)

    pygame.draw.rect(window, white,(paddle.paddle1_pos[0], 200, paddle.paddle_width, paddle.paddle_height))
    pygame.draw.rect(window, white,(paddle.paddle2_pos[0], 100, paddle.paddle_width, paddle.paddle_height))
    pygame.draw.rect(window, white, (325, 340, ball.ball_radius, ball.ball_radius))

    pygame.draw.rect(window, white, (22, 379, mid * 2 - 43, 15))
    pygame.draw.rect(window, white, (22, 364, 8, 15))
    pygame.draw.rect(window, white, (30, 369, 40, 10))
    pygame.draw.rect(window, white, (62, 373, 20, 6))
    pygame.draw.rect(window, white, (82, 364, 30, 15))
    pygame.draw.rect(window, white, (132, 367, 30, 12))
    pygame.draw.rect(window, white, (162, 354, 40, 25))
    pygame.draw.rect(window, white, (202, 365, 80, 14))
    pygame.draw.rect(window, white, (282, 373, 90, 6))
    pygame.draw.rect(window, white, (372, 367, 50, 12))
    pygame.draw.rect(window, white, (422, 362, 40, 18))
    pygame.draw.rect(window, white, (462, 357, 30, 22))
    pygame.draw.rect(window, white, (492, 366, 55, 13))
    pygame.draw.rect(window, white, (546, 371, 34, 8))


def main_menu():
    global is_play_screen
    global is_setting
    global is_high_score

    draw_main()
    mouse = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()

    colora = white
    colorb = white
    colorc = white

    # originally used rectangles to determine the boundaries of the buttons
    # pygame.draw.rect(window, color, (mid - 130, 25, 260, 75))
    # pygame.draw.rect(window, color, (mid - 82, 120, 160, 55))
    # pygame.draw.rect(window, color, (mid - 142, 195, 300, 55))
    # pygame.draw.rect(window, color, (mid - 190, 270, 400, 55))

    # for button; if the mouse cursor is within a certain range (range of button).
    if mid - 82 < mouse[0] < mid - 82 + 160 and 120 < mouse[1] < 120 + 55:
        colora = gold
        # if the mouse is clicked
        if press[0] == 1:
            is_play_screen = True

    elif mid - 142 < mouse[0] < mid - 142 + 300 and 195 < mouse[1] < 195 + 55:
        colorb = gold
        if press[0] == 1:
            is_setting = True

    elif mid - 190 < mouse[0] < mid - 190 + 400 and 270 < mouse[1] < 270 + 55:
        colorc = gold
        if press[0] == 1:
            is_high_score = True

    help_button()

    render_text("PONG", mainfont, white, mid - 120, 45)
    render_text("PLAY", subfont, colora, mid - 70, 133)
    render_text("SETTINGS", subfont, colorb, mid - 130, 208)
    render_text("HIGH SCORES", subfont, colorc, mid - 180, 280)


def esc_button():
    global is_play_screen
    global is_setting
    global is_high_score
    global is_help

    color = white
    mouse = pygame.mouse.get_pos()
    if 510 < mouse[0] < 580 and 6 < mouse[1] < 36:
        color = gold
        if pygame.mouse.get_pressed()[0] == 1:
            # resets values
            is_play_screen = False
            is_setting = False
            is_high_score = False
            is_help = False
    draw_box(510, 6, 70, 30, 3, white)
    render_text("esc", escfont, color, 519, 12)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        is_play_screen = False
        is_setting = False
        is_high_score = False
        is_help = False


def play_screen():
    window.fill(black)
    esc_button()

    global one_player
    global color1
    global color2
    global color3
    global color4
    global color5
    global color6
    global color7
    global color8
    global color9
    global color10
    global color11
    global game_key
    global bot
    global score_limit
    global mode
    global prob
    global slow
    global score_select

    mouse = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()
    if press[0] == 1:
        if 70 < mouse[0] < 285 and 130 < mouse[1] < 180:
            color1 = gold
            color2 = white
            one_player = True

        elif 315 < mouse[0] < 530 and 130 < mouse[1] < 180:
            color1 = white
            color2 = gold
            one_player = False

        elif 315 < mouse[0] < 530 and 220 < mouse[1] < 270:
            color3 = white
            color4 = gold
            mode = 2

        elif 70 < mouse[0] < 285 and 220 < mouse[1] < 270:
            color3 = gold
            color4 = white
            mode = 1

    GameWindow.draw_main_box(game)

    # first box
    draw_box(50, 120, 500, 70, 2, white)
    render_text("# of Players", tinyfont, white, 50, 105)

    # second box
    draw_box(50, 210, 500, 70, 2, white)
    render_text("Mode Type", tinyfont, white, 50, 195)

    # third box
    draw_box(50, 300, 500, 70, 2, white)

    # first, first box
    draw_box(70, 130, 215, 50, 2, color1)
    render_text("1 PLAYER", boxfont, white, 77, 145)

    # first, second box
    draw_box(315, 130, 215, 50, 2, color2)
    render_text("2 PLAYER", boxfont, white, 322, 145)

    # second, first box
    draw_box(70, 220, 215, 50, 2, color3)
    render_text("CLASSIC", boxfont, white, 87, 235)

    # second, second box
    draw_box(315, 220, 215, 50, 2, color4)
    render_text("ARCADE", boxfont, white, 347, 235)

    # if there is only one player, than the selection should be different
    if one_player is True:
        render_text("BOT Difficulty", tinyfont, white, 50, 285)
        score_select = 0
        score_limit = 10
        if press[0] == 1:
            if 72 < mouse[0] < 212 and 310 < mouse[1] < 360:
                bot = 1
                color5 = gold
                color6 = white
                color7 = white
            elif 227 < mouse[0] < 367 and 310 < mouse[1] < 360:
                bot = 2
                color5 = white
                color6 = gold
                color7 = white
            elif 382 < mouse[0] < 552 and 310 < mouse[1] < 360:
                bot = 3
                color5 = white
                color6 = white
                color7 = gold

        # third, first box
        draw_box(72, 310, 140, 50, 2, color5)
        render_text("EASY", boxfont, white, 92, 325)

        # third, second box
        draw_box(227, 310, 140, 50, 2, color6)
        render_text("FAIR", boxfont, white, 247, 325)

        # third, third box
        draw_box(382, 310, 140, 50, 2, color7)
        render_text("HARD", boxfont, white, 402, 325)

    elif one_player is False:
        render_text("Score Limit", tinyfont, white, 50, 285)
        if press[0] == 1:
            if 70 < mouse[0] < 285 and 310 < mouse[1] < 360:
                score_limit = 1000
                color8 = gold
                color9 = white
                color10 = white
                color11 = white
                score_select = 1
            elif 300 < mouse[0] < 370 and 310 < mouse[1] < 360:
                score_limit = 50
                color8 = white
                color9 = gold
                color10 = white
                color11 = white
                score_select = 1
            elif 385 < mouse[0] < 455 and 310 < mouse[1] < 360:
                score_limit = 25
                color8 = white
                color9 = white
                color10 = gold
                color11 = white
                score_select = 1
            elif 470 < mouse[0] < 540 and 310 < mouse[1] < 360:
                score_limit = 10
                color8 = white
                color9 = white
                color10 = white
                color11 = gold
                score_select = 1

        # third, first box
        draw_box(70, 310, 215, 50, 2, color8)
        render_text("NO LIMIT", boxfont, white, 81, 325)

        # third, second box
        draw_box(300, 310, 70, 50, 2, color9)
        render_text("50", boxfont, white, 312, 325)

        # third, third box
        draw_box(385, 310, 70, 50, 2, color10)
        render_text("25", boxfont, white, 397, 325)

        # third, fourth box
        draw_box(470, 310, 60, 50, 2, color11)
        render_text("10", boxfont, white, 476, 325)

    # determines the element needed for the bot
    # easy level
    if bot == 1:
        prob = 50
        slow = 0
    # fair level
    elif bot == 2:
        prob = 70
        slow = 2
    # hard level
    elif bot == 3:
        prob = 90
        slow = 4

    global ai
    ai = AI(prob, slow)

    # if not every selection has been checked, then the "Play" button turns red to signal user

    true_color = white
    # for button; if the mouse cursor is within a certain range (range of button).
    if mid - 130 < mouse[0] < mid - 130 + 260 and 25 < mouse[1] < 25 + 75:
        true_color = gold
        # if mouse is clicked
        if press[0] == 1:
            if mode > 0 and ((one_player is True and bot > 0) or (one_player is False and score_select > 0)):
                game_key = True
            else:
                true_color = red
    render_text("PLAY", mainfont, true_color, mid - 120, 38)


def reset_hs():
    global is_new_hs
    is_new_hs = False

    # loads scores into the seperate file
    hs.load_scores()


def reset():
    # resets values
    global is_pause
    global color1
    global color2
    global color3
    global color4
    global color5
    global color6
    global color7
    global color8
    global color9
    global color10
    global color11

    if is_new_hs is True:
        reset_hs()
    is_pause = False

    ball.start_game()
    score.p1_score = 0
    score.p2_score = 0

    color1 = gold
    color2 = white
    color3 = white
    color4 = white
    color5 = white
    color6 = white
    color7 = white
    color8 = white
    color9 = white
    color10 = white
    color11 = white


def reset_full():
    # resets other values
    global is_play_screen
    global game_key
    global bot
    global score_limit
    global mode
    global score_select
    global one_player
    global is_high_score
    reset()
    is_play_screen = False
    is_high_score = False
    game_key = False
    bot = 0
    mode = 0
    score_limit = 0
    score_select = 0
    one_player = True


def menu_button(y, effect):
    # x position is always in the middle; y position varies.
    # 'effect' is the desirable effect when button is pressed

    mouse = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()
    color = white
    if 150 < mouse[0] < 450 and y < mouse[1] < y + 60:
        color = gold
        if pygame.mouse.get_pressed()[0] == 1 or key[pygame.K_RETURN]:
            effect()
    elif key[pygame.K_RETURN]:
        effect()

    draw_box(150, y, 300, 60, 2, white)
    render_text("MAIN MENU", menufont, color, 166, y + 18)
    render_text("PRESS ENTER", smallfont, white, 188, y - 24)


def settings_screen():
    global primary_color
    global secondary_color

    mouse = pygame.mouse.get_pos()
    window.fill(black)
    GameWindow.draw_main_box(game)
    esc_button()

    if pygame.mouse.get_pressed()[0] == 1:
        if primary_color != secondary_color:

            # buttons for selecting different colors
            if 304 < mouse[0] < 354 and 85 < mouse[1] < 135:
                primary_color = black
            elif 364 < mouse[0] < 414 and 85 < mouse[1] < 135:
                primary_color = white
            elif 304 < mouse[0] < 354 and 145 < mouse[1] < 195:
                primary_color = green
            elif 364 < mouse[0] < 414 and 145 < mouse[1] < 195:
                primary_color = yellow
            elif 304 < mouse[0] < 354 and 205 < mouse[1] < 255:
                primary_color = orange
            elif 364 < mouse[0] < 414 and 205 < mouse[1] < 255:
                primary_color = red
            elif 304 < mouse[0] < 354 and 265 < mouse[1] < 315:
                primary_color = pink
            elif 364 < mouse[0] < 414 and 265 < mouse[1] < 315:
                primary_color = light_blue
            elif 304 < mouse[0] < 354 and 325 < mouse[1] < 375:
                primary_color = purple
            elif 364 < mouse[0] < 414 and 325 < mouse[1] < 375:
                primary_color = blue

            if 444 < mouse[0] < 494 and 85 < mouse[1] < 135:
                secondary_color = black
            elif 504 < mouse[0] < 554 and 85 < mouse[1] < 135:
                secondary_color = white
            elif 444 < mouse[0] < 494 and 145 < mouse[1] < 195:
                secondary_color = dull_green
            elif 504 < mouse[0] < 554 and 145 < mouse[1] < 195:
                secondary_color = dull_yellow
            elif 444 < mouse[0] < 494 and 205 < mouse[1] < 255:
                secondary_color = dull_orange
            elif 504 < mouse[0] < 554 and 205 < mouse[1] < 255:
                secondary_color = dull_red
            elif 444 < mouse[0] < 494 and 265 < mouse[1] < 315:
                secondary_color = dull_pink
            elif 504 < mouse[0] < 554 and 265 < mouse[1] < 315:
                secondary_color = dull_blue
            elif 444 < mouse[0] < 494 and 325 < mouse[1] < 375:
                secondary_color = purple
            elif 504 < mouse[0] < 554 and 325 < mouse[1] < 375:
                secondary_color = blue
        else:
            primary_color = white
            secondary_color = black

    # GUI, drawing boundaries, boxes, and filling in the boxes with different colors
    window.fill(secondary_color, rect=[30, 15, 250, 370])
    draw_box(30, 15, 250, 370, 2, primary_color)
    pygame.draw.line(window, primary_color, [30, 30], [280, 30], 2)
    pygame.draw.line(window, primary_color, [30, 370], [280, 370], 2)
    draw_middle(30, 200, 280, 200, 13, 12, primary_color)
    pygame.draw.rect(window, primary_color, (110, 40, 80, 12))
    pygame.draw.rect(window, primary_color, (110, 350, 80, 12))
    pygame.draw.rect(window, primary_color, (190, 160, 15, 15))
    render_text("o", subfont, primary_color, 50, 130)
    render_text("o", subfont, primary_color, 50, 236)
    draw_box(297, 75, 125, 310, 2, white)
    draw_box(437, 75, 125, 310, 2, white)
    draw_many_boxes(304, 85, 50, 50, 2, white, 10, 10, 2, 5)
    draw_many_boxes(444, 85, 50, 50, 2, white, 10, 10, 2, 5)
    render_text("COLORS", subfont, white, 293, 25)

    window.fill(black, rect=[306, 87, 48, 48])
    window.fill(white, rect=[366, 87, 48, 48])
    window.fill(green, rect=[306, 147, 48, 48])
    window.fill(yellow, rect=[366, 147, 48, 48])
    window.fill(orange, rect=[306, 207, 48, 48])
    window.fill(red, rect=[366, 207, 48, 48])
    window.fill(pink, rect=[306, 267, 48, 48])
    window.fill(light_blue, rect=[366, 267, 48, 48])
    window.fill(purple, rect=[306, 327, 48, 48])
    window.fill(blue, rect=[366, 327, 48, 48])

    window.fill(black, rect=[446, 87, 48, 48])
    window.fill(white, rect=[506, 87, 48, 48])
    window.fill(dull_green, rect=[446, 147, 48, 48])
    window.fill(dull_yellow, rect=[506, 147, 48, 48])
    window.fill(dull_orange, rect=[446, 207, 48, 48])
    window.fill(dull_red, rect=[506, 207, 48, 48])
    window.fill(dull_pink, rect=[446, 267, 48, 48])
    window.fill(dull_blue, rect=[506, 267, 48, 48])
    window.fill(purple, rect=[446, 327, 48, 48])
    window.fill(blue, rect=[506, 327, 48, 48])


class HS(object):
    def __init__(self, first, second, third, color1, color2, color3, name):
        self.first = first
        self.second = second
        self.third = third
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.name = name

    @staticmethod
    def high_score_screen():
        window.fill(black)
        GameWindow.draw_main_box(game)
        esc_button()

        saved_hs = pickle.load(open("top_scores.rtf", "rb"))
        # c is the count of the five available high score spots, and y is the y position of the score on the screen
        c = 0
        y = 0
        while c < 5:
            if saved_hs["scores"][c] >= 10:
                # space is how many zeroes are needed to be in the front of the number: 005 (2 zeroes) and 015 (1 zero)
                space = "0"
            if saved_hs["scores"][c] <= 9:
                space = "00"

            new_score = "{}   {} - {}{} - {}".format(c+1, saved_hs["names"][c], space, saved_hs["scores"][c], saved_hs["mode"][c])
            render_text(new_score, smallfont, white, 100, 140 + y)
            y += 45
            c += 1

        render_text("HIGH SCORES", menufont, white, 130, 20)
        render_text("HARD LEVEL", boxfont, white, 176, 63)

    @staticmethod
    def load_scores():
        # decides what mode it was and if the bot played against was on hard difficulty (only hard dif gets saved)
        if bot == 3:
            # inserts into the last ranked high score
            top_scores["scores"][4] = score.p1_score
            top_scores["names"][4] = str(hs.name)
            if mode == 1:
                top_scores["mode"][4] = "CLA"
            elif mode == 2:
                top_scores["mode"][4] = "ARC"

            # then sorts them out
            hs.sort()

            # saves onto separate file
            pickle.dump(top_scores, open("top_scores.rtf", "wb"))

    @staticmethod
    def sort():
        global top_scores
        for x in range(0, 4):
            minIndex = x
            for j in range(x + 1, 5):
                if top_scores["scores"][j] > top_scores["scores"][minIndex]:
                    minIndex = j
            if minIndex != x:
                top_scores["scores"][x], top_scores["scores"][minIndex] = top_scores["scores"][minIndex],top_scores["scores"][x]
                top_scores["names"][x], top_scores["names"][minIndex] = top_scores["names"][minIndex], top_scores["names"][x]
                top_scores["mode"][x], top_scores["mode"][minIndex] = top_scores["mode"][minIndex], top_scores["mode"][x]

    def new_high_score(self):
        global is_first
        global is_second
        global is_new_hs
        global is_pause

        is_pause = False
        is_new_hs = True
        window.fill(black)
        GameWindow.draw_main_box(game)
        menu_button(320, reset_full)
        render_text("CONGRATULATIONS!", menufont, white, 67, 22)
        victory_text = "{} - {}".format(score.p1_score, score.p2_score)
        render_text(victory_text, boxfont, white, 237, 80)
        render_text("NEW HIGH SCORE ACHIEVED!", smallfont, white, 65, 136)
        render_text("ENTER YOUR NAME: ", smallfont, white, 45, 200)

        keys = pygame.key.get_pressed()
        if is_first is True:
            if keys[pygame.K_UP]:
                # delay needed so that if a user presses key button the letters will change one by one.
                pygame.time.delay(150)
                if self.first < 90:
                    # originally stores letters in numbers for latter conversion
                    self.first += 1
            elif keys[pygame.K_DOWN]:
                pygame.time.delay(150)
                if self.first > 65:
                    self.first -= 1

        if keys[pygame.K_2] and is_first is True:
            self.color1 = white
            self.color2 = gold
            is_first = False
            is_second = True

        if is_second is True:
            if keys[pygame.K_UP]:
                pygame.time.delay(150)
                if self.second < 90:
                    self.second += 1

            elif keys[pygame.K_DOWN]:
                pygame.time.delay(150)
                if self.second > 65:
                    self.second -= 1

        if keys[pygame.K_3] and is_second is True:
            self.color2 = white
            self.color3 = gold
            is_second = False
            is_first = False

        if is_second is False and is_first is False:
            if keys[pygame.K_UP]:
                pygame.time.delay(150)
                if self.third < 90:
                    self.third += 1

            elif keys[pygame.K_DOWN]:
                pygame.time.delay(150)
                if self.third > 65:
                    self.third -= 1

        if keys[pygame.K_1] and is_second is False and is_first is False:
            self.color3 = white
            self.color1 = gold
            is_first = True
            is_second = False

        render_text("PRESS", tinyfont, white, 300, 169)
        render_text("1", tinyfont, white, 390, 169)
        render_text("2", tinyfont, white, 440, 169)
        render_text("3", tinyfont, white, 490, 169)

        # 'chr' converts the numbers into letters
        render_text(chr(self.first), subfont, self.color1, 380, 187)
        render_text(chr(self.second), subfont, self.color2, 430, 187)
        render_text(chr(self.third), subfont, self.color3, 480, 187)

        render_text("PRESS SPACE TO PLAY AGAIN", smallfont, white, 58, 255)

        self.name = "{}{}{}".format(chr(self.first), chr(self.second), chr(self.third))

        if keys[pygame.K_SPACE]:
            reset()


def draw_many_boxes(x, y, width, height, thick, color, xinterval, yinterval, xamount, yamount):
    xcount = 0
    x1 = x
    while xcount < xamount:
        ycount = 0
        y1 = y
        while ycount < yamount:
            draw_box(x1, y1, width, height, thick, color)
            y1 += yinterval + height
            ycount += 1
        x1 += xinterval + width
        xcount += 1


def draw_middle(x1, y1, x2, y2, length, space, color):
    count = 0
    distance = x2 - x1
    interval = length + space
    limit = int(distance/interval)
    x1 += 5
    while count < limit:
        x = x1 + interval * count
        pygame.draw.line(window, color, [x, y1], [length + x, y2], 2)
        count += 1


def victory_screen():
    window.fill(black)
    menu_button(300, reset_full)
    GameWindow.draw_main_box(game)
    victory_font = pygame.font.Font(font_path, 40)
    if score.p1_score > score.p2_score:
        render_text("PLAYER 1 WINS", victory_font, white, 42, 24)
    elif score.p1_score < score.p2_score:
        render_text("PLAYER 2 WINS", victory_font, white, 42, 24)
    victory_text = "{} - {}".format(score.p1_score, score.p2_score)
    render_text(victory_text, subfont, white, 209, 105)
    render_text("PRESS SPACE TO PLAY AGAIN", smallfont, white, 58, 200)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        reset()


def pause_screen():
    global is_pause
    window.fill(black)
    GameWindow.draw_main_box(game)
    render_text("PAUSE", mainfont, white, 155, 20)
    render_text("PRESS SPACE TO CONTINUE", smallfont, white, 72, 165)

    # checks whether the player is qualified to receive a high score in the current pause state
    if one_player is True and bot == 3 and score.p1_score > top_scores["scores"][4]:
        # if the player is achieving a high score but decides to go to main menu, instead redirected to new_hs_screen
        menu_button(275, hs.new_high_score)
    else:
        # otherwise redirected to main menu
        menu_button(275, reset_full)


def pause():
    global is_pause
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        is_pause = True
    if keys[pygame.K_SPACE]:
        is_pause = False


class Arcade(object):
    def __init__(self, box_thick, appearance, disappear, xcade, ycade, start, effect_length):
        self.box_thick = box_thick
        self.appearance = appearance
        self.disappear = disappear
        self.xcade = xcade
        self.ycade = ycade
        self.start = start
        self.effect_length = effect_length

    def time(self):
        global is_hit_box
        global is_appear
        # 100 units here equals to one second.
        if self.start > 0:
            self.start -= 1
        if self.start <= 0:
            if is_appear is True and self.disappear <= 1:
                # this makes the spawning position of the mystery box random
                self.xcade = random.randint(50, 510)
                self.ycade = random.randint(10, 350)
            if self.appearance > 0:
                draw_box(self.xcade, self.ycade, self.box_thick, self.box_thick, 2, primary_color)
                render_text("?", subfont, primary_color, self.xcade + 5, self.ycade + 5)
            is_appear = False
            if self.appearance <= 0:
                is_appear = True
                self.xcade = 0
                self.ycade = 0
                if is_hit_box is True:
                    # 100 units here equals to one second. So 1000 is 10 seconds.
                    self.disappear = 1000
                    is_hit_box = False
            if self.disappear > 0 and is_hit_box is False:
                self.disappear -= 1
            if self.disappear <= 0:
                self.appearance = 400
                is_hit_box = True
                self.disappear = 1
            if self.appearance > 0:
                self.appearance -= 1

        # because these continuous calculations take much processing power,for game to be smooth fps has to be increased
        fps.tick(250)

    def arcade_collision(self):
        global is_hit_box
        global arcade_effect

        xcade = self.xcade
        ycade = self.ycade

        ball_pos = ball.ball_pos
        radius = ball.ball_radius
        thick = self.box_thick
        if xcade <= ball_pos[0] <= xcade + thick or xcade <= ball_pos[0] + radius <= xcade + thick or arcade_effect is True:
            if ycade <= ball_pos[1] <= ycade + thick or ycade <= ball_pos[1] + radius <= ycade + thick or arcade_effect is True:
                self.appearance = 0
                arcade_effect = True
                arcade.effects()

    def effects(self):
        global secondary_color
        global previous_s_color
        global change_length
        global normal_move_paddle
        global spin

        global is_spin

        # it has to spin only once and that value should remain. So as soon as it spins, it should wait until next
        if is_spin is True:
            spin = random.randint(1, 3)
            is_spin = False

        if self.effect_length >= 0:
            time = self.effect_length / 100
            render_text(time, smallfont, primary_color, 490, 16)
            self.effect_length -= 1
            if spin == 1:
                # simply increasing the speed by two.
                render_text("SUPER SPEED!", tinyfont, primary_color, 28, 13)
                ball.ball_speed *= 2

                # for balance, the doubled speed should not exceed 19
                if ball.ball_speed > 19:
                    ball.ball_speed = 19
            elif spin == 2:
                render_text("RAINBOW LAND!", tinyfont, primary_color, 28, 13)

                # changes the duration of the effect
                if change_length is True:
                    # also remembers the set color so that it can be recalled later
                    previous_s_color = secondary_color
                    # time of effect lasting
                    self.effect_length = 600
                change_length = False

                # time frames for changing into different colors
                if 550 < self.effect_length < 600:
                    secondary_color = dull_blue
                elif 500 < self.effect_length < 550:
                    secondary_color = dull_orange
                elif 450 < self.effect_length < 500:
                    secondary_color = dull_green
                elif 400 < self.effect_length < 450:
                    secondary_color = dull_yellow
                elif 350 < self.effect_length < 400:
                    secondary_color = dull_pink
                elif 300 < self.effect_length < 350:
                    secondary_color = dull_red
                elif 250 < self.effect_length < 300:
                    secondary_color = dull_blue
                elif 200 < self.effect_length < 250:
                    secondary_color = dull_orange
                elif 150 < self.effect_length < 200:
                    secondary_color = dull_green
                elif 100 < self.effect_length < 150:
                    secondary_color = dull_yellow
                elif 50 < self.effect_length < 100:
                    secondary_color = dull_pink
                elif 0 < self.effect_length < 50:
                    secondary_color = dull_red
            elif spin == 3:
                # simply reversing the effects of pressing the up and down (A & Z) keys
                render_text("MIRROR!", tinyfont, primary_color, 28, 13)
                normal_move_paddle = False
            '''elif spin == 4:
                render_text("DOUBLE BALL!", tinyfont, primary_color, 28, 13)
                ball.start_game()'''
        else:
            # after rainbow land, the bg color should return to its previous set color
            if spin == 2:
                secondary_color = previous_s_color
            arcade.reset_effects()
        fps.tick(500)

    def reset_effects(self):
        global arcade_effect
        global change_length
        global normal_move_paddle
        global secondary_color
        global is_spin

        # returns values into the original state
        arcade_effect = False
        self.effect_length = 500
        change_length = True
        normal_move_paddle = True
        is_spin = True

    def reset_arcade(self):
        global is_appear
        global is_hit_box

        # returns time values into original state + the other arcade values
        is_hit_box = True
        is_appear = True
        self.start = 500
        self.appearance = 400
        self.disappear = 1
        self.xcade = 0
        self.ycade = 0
        arcade.reset_effects()


def instructions_screen():
    # this section is simply GUI; no algorithms
    window.fill(black)
    game.draw_main_box()
    esc_button()
    pygame.draw.rect(window, white, (paddle.paddle1_pos[0], 165, paddle.paddle_width, paddle.paddle_height))
    pygame.draw.rect(window, white, (paddle.paddle2_pos[0], 165, paddle.paddle_width, paddle.paddle_height))
    render_text("HOW TO PLAY", subfont, white, 110, 20)

    render_text("UP", smallfont, white, 55, 78)
    render_text("A", subfont, white, 55, 110)
    draw_box(45, 100, 50, 50, 2, white)

    render_text("DOWN", smallfont, white, 32, 328)
    render_text("Z", subfont, white, 55, 280)
    draw_box(45, 270, 50, 50, 2, white)

    render_text("UP", smallfont, white, 515, 78)
    render_text("↑", subfont, white, 515, 110)
    draw_box(505, 100, 50, 50, 2, white)

    render_text("DOWN", smallfont, white, 490, 328)
    render_text("↓", subfont, white, 515, 280)
    draw_box(505, 270, 50, 50, 2, white)

    render_text("Arcade Mode:", smallfont, white, 185, 75)
    render_text("Classic Pong Game", smallfont, white, 130, 100)
    render_text("w/Mystery Boxes", smallfont, white, 150, 125)

    render_text("1 Player Mode:", smallfont, white, 160, 170)
    render_text("Game Lasts Until BOT", smallfont, white, 100, 195)
    render_text("Reaches Score of 10", smallfont, white, 110, 220)

    render_text("2 Player Mode:", smallfont, white, 160, 265)
    render_text("Game Lasts Until ", smallfont, white, 140, 290)
    render_text("A Player Reaches", smallfont, white, 140, 315)
    render_text("the Score Limit", smallfont, white, 150, 340)


def help_button():
    global is_help
    color = white
    mouse = pygame.mouse.get_pos()
    if 20 < mouse[0] < 200 and 6 < mouse[1] < 36:
        color = gold
        if pygame.mouse.get_pressed()[0] == 1:
            is_help = True

    draw_box(20, 6, 180, 30, 3, white)

    font = pygame.font.Font(font_path, 15)
    render_text("HOW TO PLAY", font, color, 29, 15)


def classic():
    # classic game functions in one function
    paddle.draw_paddles()

    game.draw_mid()
    game.draw_game_box()

    ball.wall_collision()
    ball.paddle_collision()
    ball.move_ball()

    score.score_collision()
    score.update_score()

# inputs the needed values into different classes
game = GameWindow(400, 600, 5)
paddle = Paddles(15, 90, 10)
score = Score(0, 0)
ball = Ball(15, 6)
hs = HS(65, 65, 65, gold, white, white, "NON")

arcade = Arcade(40, 400, 1, 0, 0, 500, 500) # self.start is 500 (5 seconds)

window = pygame.display.set_mode((game.screen_width, game.screen_height))
pygame.display.set_caption("Pong Game")
fps = pygame.time.Clock()

# sets the needed variables before the game starts; without this game won't work
ball.start_game()

# down bottom here because the class 'game' needs to have variables inputed
mid = game.screen_width / 2

run = True
while run:
    # original frame per second tick rate
    fps.tick(200)

    # the quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # this whole section below uses a complex web of boolean logic to determine what needs to be shown/done

    # this is the main menu section. It is on top because it is the first layer in the game.
    if is_setting is True:
        settings_screen()
    elif is_high_score is True:
        hs.high_score_screen()
    elif is_help is True:
        instructions_screen()
    elif is_play_screen is True:
        if game_key is False:
            play_screen()
        else:
            # constantly checks whether there is a pause or not; if yes, then stops game, creating true pause
            pause()
            if is_pause is True:
                pause_screen()
            elif is_new_hs is True:
                hs.new_high_score()
            else:
                # determines whether there are two players and score limit is reached. If yes, then victory screen.
                if (score.p1_score >= score_limit or score.p2_score >= score_limit) and one_player is False:
                    # 2 player end screen
                    victory_screen()

                # determines if bot reached a score of 10 and there is one player
                elif one_player is True and score.p2_score >= 10:
                    if bot == 3:
                        # then checks whether the score is higher than lowest saved high score
                        if score.p1_score > top_scores["scores"][4]:
                            hs.new_high_score()
                        else:
                            victory_screen()
                    else:
                        victory_screen()
                else:
                    # after determining whether game should end or not, looks at mode
                    keys = pygame.key.get_pressed()

                    # mode = 1 is classic mode, mode = 2 is arcade mode
                    if mode == 1:
                        classic()
                        paddle.player_move_paddle(keys[pygame.K_a], keys[pygame.K_z])
                    elif mode == 2:
                        classic()

                        # determines whether the power-up mirror is hit
                        if normal_move_paddle is True:
                            # if power up mirror is hit, then it switches up and down for player 1
                            paddle.player_move_paddle(keys[pygame.K_a], keys[pygame.K_z])
                        else:
                            paddle.player_move_paddle(keys[pygame.K_z], keys[pygame.K_a])
                        arcade.time()
                        arcade.arcade_collision()

                    # if there is one player, then there should be a bot
                    if one_player is True:
                        # checks whether there is a possibility of a new high score
                        if is_new_hs is True and bot == 3:
                            # then checks whether the score is higher than lowest saved high score
                            if score.p1_score > top_scores["scores"][4]:
                                hs.new_high_score()
                            else:
                                victory_screen()
                        else:
                            ai.bot()

                    # if there are two players, then second player should be allowed to move
                    else:
                        # checks for power up 'mirror' for the second paddle too. Bot isn't affected by mirror
                        if normal_move_paddle is True:
                            paddle.players_move_paddle(keys[pygame.K_UP], keys[pygame.K_DOWN])
                        else:
                            paddle.players_move_paddle(keys[pygame.K_DOWN], keys[pygame.K_UP])
    else:
        main_menu()

    pygame.display.update()

pygame.quit()
