import pygame
pygame.init()
import time
import math
from random import randint, choice

WIDTH = 950
HEIGHT = 620
PADDLE_VEL = 7
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_RADIUS = 12
BALL_START_X_VEL = 6
BALL_MAX_Y_VEL = 7
SCORE_2_WIN = 7
GAME_START_TIME = time.time()
PURPLE = (209, 26, 255)
ORANGE = (255, 117, 26)
FREQ_OF_POWER = 10
POWER_BALL_RADIUS = 17
LIFE_TIME_POWER_BALL = 9
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (9, 239, 239)
POWER_LIST = ['power', 'blinking_ball', 'large', 'small', 'twin']
POWER_COLOR_MAP = {POWER_LIST[0]:PURPLE, POWER_LIST[1]:RED, POWER_LIST[2]:GREEN, POWER_LIST[3]:ORANGE, POWER_LIST[4]:BLUE}

FONT = pygame.font.SysFont("Times New Roman", 30)
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ping pong")

class Paddel:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = "white"
        self.is_hit_ball = False
        self.velocity = PADDLE_VEL
        self.score = 0


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0, 2)

    def move_up(self):
        self.y -= self.velocity

    def move_down(self):
        self.y += self.velocity
    
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = BALL_START_X_VEL * choice([-1, 1])
        self.y_vel = randint(-3, 3)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move_x(self):
        self.x += self.x_vel

    def move_y(self):
        self.y += self.y_vel

    def collusion(self, ball):
        distance_between_ball_center = math.sqrt((ball.x - self.x)**2 + (ball.y - self.y)**2)
        if distance_between_ball_center <= ball.radius + self.radius:
            return True
        else:
            return False

def color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def draw(win, paddle_1, paddle_2, balls, power_balls):
    win.fill("black")
    pygame.draw.line(win, "white", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.circle(win, "white", (WIDTH // 2, HEIGHT //2), 40, 2)
    starting_x = WIDTH // 2 - 170
    player_1_score = paddle_1.score
    for i in range(SCORE_2_WIN):
        if player_1_score:
            player_1_score -= 1
            pygame.draw.circle(win, "white", (starting_x, 20), 10)
        else:    
            pygame.draw.circle(win, "white", (starting_x, 20), 10, 2)
        starting_x += 25
    starting_x = WIDTH // 2 + 23
    player_2_score = SCORE_2_WIN - paddle_2.score
    for i in range(SCORE_2_WIN):
        if player_2_score:
            player_2_score -= 1
            pygame.draw.circle(win, "white", (starting_x, 20), 10, 2)
        else:
            pygame.draw.circle(win, "white", (starting_x, 20), 10)
        starting_x += 25
    paddle_1.draw(win)
    paddle_2.draw(win)
    for ball in balls:
        ball.draw(win)
    for power_ball in power_balls:
        power_ball.draw(win)
    pygame.display.update()
    
def paddle_movement(keys, paddle_1, paddle_2):
    if keys[pygame.K_w] and paddle_1.y > 0:
        paddle_1.move_up()
    if keys[pygame.K_s] and paddle_1.y + paddle_1.height < HEIGHT:
        paddle_1.move_down()
    if keys[pygame.K_UP] and paddle_2.y > 0:
        paddle_2.move_up()
    if keys[pygame.K_DOWN] and paddle_2.y + paddle_2.height < HEIGHT:
        paddle_2.move_down()
           
def ball_movement(keys, paddle_1 , paddle_2, balls):
    for ball in balls:
        ball.move_x()
        ball.move_y()

        if ball.y + ball.radius + (ball.y_vel // 2) >= HEIGHT or ball.y - ball.radius <= -ball.y_vel // 2:
            ball.y_vel = -ball.y_vel

        if ball.x + ball.radius + (ball.x_vel // 2) >= paddle_2.x and ball.y in range(paddle_2.y, paddle_2.y + paddle_2.height + 1):
            #for purple power
            if paddle_2.color == PURPLE and ball.x_vel <= 24:
                ball.x_vel = int(ball.x_vel * 1.9) 
            if paddle_2.color != PURPLE and ball.x_vel > 12:
                ball.x_vel //= 1.3

            ball.x_vel = -ball.x_vel
            dis = ball.y - (paddle_2.y + paddle_1.height // 2)
            if keys[pygame.K_UP]:
                dis -= 2
            elif keys[pygame.K_DOWN]:
                dis += 2
            ball.y_vel = BALL_MAX_Y_VEL * dis // 40

        elif ball.x - ball.radius + (ball.x_vel // 2) <= paddle_1.x + paddle_1.width and ball.y in range(paddle_1.y, paddle_1.y + paddle_1.height + 1):
            #for purple power
            if paddle_1.color == PURPLE and ball.x_vel >= -24:
                ball.x_vel = int(ball.x_vel * 1.9)
            if paddle_1.color != PURPLE and ball.x_vel < -12:
                ball.x_vel //= 1.3

            ball.x_vel = -ball.x_vel
            dis = ball.y - (paddle_1.y + paddle_1.height // 2)
            if keys[pygame.K_w]:
                dis -= 2
            elif keys[pygame.K_s]:
                dis += 2
            ball.y_vel = BALL_MAX_Y_VEL * dis // 40

def score_count(paddle_1, paddle_2, balls):
    hit = False
    i = 0
    while i < len(balls):
        ball = balls[i]
        if ball.x + ball.radius >= WIDTH:
            paddle_1.score += 1
            if len(balls) == 2:
                balls.pop(i)
            else:
                ball.x = WIDTH // 2
                ball.y = HEIGHT // 2
                ball.x_vel = BALL_START_X_VEL
                ball.y_vel = 0
                hit = True
        if ball.x - ball.radius <= 0:
            paddle_2.score += 1
            if len(balls) == 2:
                balls.pop(i)
            else:
                ball.x = WIDTH // 2
                ball.y = HEIGHT // 2
                ball.x_vel = BALL_START_X_VEL
                ball.y_vel = 0
                hit = True
        i += 1

    if hit:   #to reset size after round
        ball = balls[0]
        paddle_1.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        paddle_2.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        paddle_1.height = PADDLE_HEIGHT
        paddle_1.color = "white"
        paddle_2.height = PADDLE_HEIGHT
        paddle_2.color = "white"
        ball.x_vel = BALL_START_X_VEL * choice([-1, 1])
        ball.y_vel = randint(-3, 3)

    if paddle_1.score >= SCORE_2_WIN or paddle_2.score >= SCORE_2_WIN:
        if paddle_1.score >= SCORE_2_WIN:
            is_p1_win = True
        else:
            is_p1_win = False
        loop1 = True
        while loop1:
            clock.tick(2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            if is_p1_win:
                win_text = FONT.render("player1 own the game", 1, color(), color())
            else:
                win_text = FONT.render("player2 own the game", 1, color(), color())
            WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()        

    loop = True
    while loop and paddle_1.score < SCORE_2_WIN and paddle_2.score < SCORE_2_WIN and hit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                return False
        keys = pygame.key.get_pressed()
        any_key_font = FONT.render(f"press A and LEFT ARROW to continue", 1, "green")
        WIN.blit(any_key_font, (WIDTH // 2 - any_key_font.get_width() // 2, HEIGHT //2 - any_key_font.get_height()))
        pygame.display.update()
        if keys[pygame.K_a] and keys[pygame.K_LEFT]:
            round_start_time = time.time()
            return True
    return True

def blinking_ball_power(balls, power_handeler):   #red ball
    #let blink power last for 7s
    temp = time.time() - power_handeler[2]
    if temp <= 1:
        balls[0].color = (0, 0, 0)
    elif temp <= 1.5:
        balls[0].color = (255, 255, 255)
    elif temp <= 2.5:
        balls[0].color = (0, 0, 0)
    elif temp <= 3:
        balls[0].color = (255, 255, 255)
    elif temp <= 4:
        balls[0].color = (0, 0, 0)
    elif temp <= 4.5:
        balls[0].color = (255, 255, 255)
    elif temp <= 5.5:
        balls[0].color = (0, 0, 0)
    elif temp <= 6:
        balls[0].color = (255, 255, 255)
    elif temp <= 7:
        balls[0].color = (0, 0, 0)
    else:
        power_handeler[1] = None
        balls[0].color = "white"

def large_paddle_power(paddle_1, paddle_2, power_handeler):
    paddle_large_size = int(PADDLE_HEIGHT * 1.3)
    power_handeler[1] = None
    if power_handeler[3] == 1:
        paddle_1.color = "green"
        if paddle_1.height == PADDLE_HEIGHT:
            paddle_1.height = paddle_large_size
        elif paddle_1.height < PADDLE_HEIGHT:
            paddle_1.height = PADDLE_HEIGHT
    elif power_handeler[3] == 2:
        paddle_2.color = "green"
        if paddle_2.height == PADDLE_HEIGHT:
            paddle_2.height = paddle_large_size
        elif paddle_2.height < PADDLE_HEIGHT:
            paddle_2.height = PADDLE_HEIGHT

def small_paddle_power(paddle_1, paddle_2, power_handeler):
    paddle_small_size = int(PADDLE_HEIGHT * 0.7)
    power_handeler[1] = None
    if power_handeler[3] == 1:
        paddle_1.color = ORANGE
        if paddle_1.height == PADDLE_HEIGHT:
            paddle_1.height = paddle_small_size
        elif paddle_1.height > PADDLE_HEIGHT:
            paddle_1.height = PADDLE_HEIGHT
    elif power_handeler[3] == 2:
        paddle_2.color = ORANGE
        if paddle_2.height == PADDLE_HEIGHT:
            paddle_2.height = paddle_small_size
        elif paddle_2.height > PADDLE_HEIGHT:
            paddle_2.height = PADDLE_HEIGHT

def power_ball_power(paddle_1, paddle_2, power_handeler):
    if power_handeler[3] == 1:
        paddle_1.color = PURPLE
    if power_handeler[3] == 2:
        paddle_2.color = PURPLE

    if time.time() - power_handeler[2] > 6:
        power_handeler[1] = None
        paddle_1.color = "white"
        paddle_2.color = "white"

def power_ball_spawn(is_power_ball_present,power_handeler, balls, power_balls):
    if not is_power_ball_present:
        if FREQ_OF_POWER < time.time() - power_handeler[0]:
            power_ball_spawned = True
            type_of_power = choice(POWER_LIST)
            color_chosen = POWER_COLOR_MAP[type_of_power]
            if color_chosen == BLUE:
                x = WIDTH // 2
                y = HEIGHT // 2
                ball_x_vel = 0
                power_ball = Ball(x, y, POWER_BALL_RADIUS + 2, color_chosen)
                power_ball.y_vel = BALL_MAX_Y_VEL - 3
            else:
                x = randint(WIDTH // 9, WIDTH - (WIDTH // 9))
                y = randint(30 + POWER_BALL_RADIUS, HEIGHT - (30 + POWER_BALL_RADIUS))
                ball_x_vel = 4
                power_ball = Ball(x, y, POWER_BALL_RADIUS, color_chosen)
            power_ball.x_vel = ball_x_vel
            power_balls.append(power_ball)
            global power_spawn_time
            power_spawn_time = time.time()
            return  power_ball_spawned
    else:
        #for power ball movement
        power_balls[0].move_x()
        power_balls[0].move_y()
        if (power_balls[0].y + power_balls[0].radius + (power_balls[0].y_vel // 2) >= HEIGHT) or (power_balls[0].y - power_balls[0].radius <= -power_balls[0].y_vel // 2):
            power_balls[0].y_vel *= -1
        if (power_balls[0].x + power_balls[0].radius >= WIDTH) or (power_balls[0].x - power_balls[0].radius <= 0):
            power_balls[0].x_vel *= -1

        for ball in balls:
            if ball.collusion(power_balls[0]):
                if ball.x_vel > 0:
                    power_handeler[3] = 1
                else:
                    power_handeler[3] = 2
                power_handeler[2] = time.time()
                if power_balls[-1].color == PURPLE:
                    power_handeler[1] = POWER_LIST[0]
                elif power_balls[-1].color == RED:
                    power_handeler[1] = POWER_LIST[1]
                elif power_balls[-1].color == GREEN:
                    power_handeler[1] = POWER_LIST[2]
                elif power_balls[-1].color == ORANGE:
                    power_handeler[1] = POWER_LIST[3]
                else:
                    power_handeler[1] = POWER_LIST[4]
                power_balls.pop()
                power_handeler[0] = time.time() - 3     #for cool down
                return False
        if time.time() - power_spawn_time > LIFE_TIME_POWER_BALL:
            power_balls.pop()
            power_handeler[0] = time.time() - 3
            return False
        return True

def main():
    running = True
    paddle_1 = Paddel(10)
    paddle_2 = Paddel(WIDTH - 10 - paddle_1.width)
    balls = []
    power_balls = []
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, "white")
    balls.append(ball)
    #power
    power_handeler = [time.time(), None, None, None]#when power last present, what power hit by ball, power taken time, who hit the power
    is_power_ball_present = False
    global round_start_time
    round_start_time = round(time.time(), 2)
    count = 0
    while running:
        clock.tick(60)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        paddle_movement(keys, paddle_1, paddle_2)
        #ball speedup
        if (round(time.time(), 2) - round_start_time) % 8 == 0 and math.fabs(ball.x_vel) < 12:
            if ball.x_vel > 0:
                ball.x_vel += 1
            else:
                ball.x_vel -= 1
        ball_movement(keys, paddle_1, paddle_2, balls)
        running = score_count(paddle_1, paddle_2, balls)
        is_power_ball_present = power_ball_spawn(is_power_ball_present,power_handeler, balls, power_balls)
        if power_handeler[1]:
            if power_handeler[1] == POWER_LIST[0]: #purple power
                power_ball_power(paddle_1, paddle_2, power_handeler)
            elif power_handeler[1] == POWER_LIST[1]: #blinking_ball red
                blinking_ball_power(balls, power_handeler)
            elif power_handeler[1] == POWER_LIST[2]: #large paddle (green power)
                large_paddle_power(paddle_1, paddle_2, power_handeler)
            elif power_handeler[1] == POWER_LIST[3]: #small paddle (orange power)
                small_paddle_power(paddle_1, paddle_2, power_handeler)
            elif power_handeler[1] == POWER_LIST[4]: #twin power
                if len(balls) < 3:
                    x = balls[0].x
                    y = balls[0].y
                    new_ball =  Ball(x, y, BALL_RADIUS, "white")
                    new_ball.x_vel = -(balls[0].x_vel)
                    new_ball.y_vel = balls[0].y_vel
                    balls.append(new_ball)
                    power_handeler[1] = None
        draw(WIN, paddle_1, paddle_2, balls, power_balls)
        count += 1
        if count > 60:
            print(power_handeler)
            print(f"x_vel : {ball.x_vel},  y_vel:{ball.y_vel}")
            count = 0
    

if __name__ == "__main__":
    main()
    pygame.quit()
