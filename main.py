#1234567890123456789012345678901234567890123456789012345678901234567890123456789
import random, copy, pygame, sys, os, math, time, asyncio
from enemy import Enemy
from imageBlur import blurScreen

### TEMPLATE FUNCTIONS

def resource_path(relative_path):

    if PLAT_VER != "WEB":
    
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    else:

        return relative_path

def log(message):
    console_log.append([str(message), FRAMERATE * 10])

def window_resize():
    resized_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    resized_window.blit(game_window, (0, 0))

    if (true_window.get_height() / true_window.get_width()) > (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen width
        resized_window = pygame.transform.scale(resized_window, (true_window.get_width(), true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT))
    elif (true_window.get_height() / true_window.get_width()) <= (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen height
        resized_window = pygame.transform.scale(resized_window, (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH, true_window.get_height()))

    font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 35)

    to_remove = []

    if console_data["Typing"]:
        text = font.render(console_data["Message"], True, (255,255,255))
        
        draw_trans_rect(resized_window, (0, 0, 0), 192, (15, resized_window.get_height() - 40, text.get_width() + 10, text.get_height()))
        resized_window.blit(text, (20, resized_window.get_height() - 40))

    if console_data["Typing"] or DEV_VER == "DEV":
        for i in range(len(console_log)):

            COLOUR = (255, 255, 0)
            TRANS = 160
            if console_log[len(console_log) - 1 - i][1] <= FRAMERATE:
                COLOUR = (192, 192, 0)
                TRANS = 128
            text = font.render(console_log[len(console_log) - 1 - i][0], True, COLOUR)

            draw_trans_rect(resized_window, (0, 0, 0), TRANS, (15, resized_window.get_height() - 67 - i * 27, text.get_width() + 10, text.get_height()))

            #pygame.draw.rect(resized_window, (0, 0, 0), (15, resized_window.get_height() - 67 - i * 25, text.get_width() + 10, text.get_height()))
            
            resized_window.blit(text, (20, resized_window.get_height() - 65 - i * 27))

            console_log[len(console_log) - 1 - i][1] -= 1
            if console_log[len(console_log) - 1 - i][1] == 0:
                to_remove.append(len(console_log) - 1 - i)

        for i in range(len(to_remove)):
            console_log.pop(0)

        if console_data["Last Command"] != "":

            text = font.render(str(console_data["Last Command"]), True, (0, 255, 255))
            draw_trans_rect(resized_window, (0, 0, 0), 192, (resized_window.get_width() - 10 - text.get_width(), 0, 10 + text.get_width(), text.get_height()))
            resized_window.blit(text, (resized_window.get_width() - 5 - text.get_width(), 0))

    if console_data["FPS"]:

        text = font.render(str(int(clock.get_fps())), True, (0, 255, 0))
        draw_trans_rect(resized_window, (0, 0, 0), 192, (resized_window.get_width() - 10 - text.get_width(), resized_window.get_height() - text.get_height(), 10 + text.get_width(), text.get_height()))
        resized_window.blit(text, (resized_window.get_width() - 5 - text.get_width(), resized_window.get_height() - text.get_height()))
    
    true_window.blit(resized_window, (true_window.get_width() // 2 - resized_window.get_width() // 2, true_window.get_height() // 2 - resized_window.get_height() // 2))

    pygame.display.update()

def global_inputs():

    non_global_inputs = []

    for event in pygame.event.get():
        handled_input = False
        
        if event.type == pygame.QUIT:
            handled_input = True
            quit_game()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                handled_input = True
                quit_game()

            if event.key == 96:
                handled_input = True
                console_data["Typing"] = not console_data["Typing"]
                        
            if event.key > 31 and event.key < 127 and event.key != 96 and console_data["Typing"]:#not backspace or weird characters
                handled_input = True
                console_data["Message"] += event.unicode #put character in text
            elif event.key == pygame.K_RETURN and console_data["Typing"]:#return
                handled_input = True
                log(console_data["Message"])
                console_data["Command"] = console_data["Message"]
                console_data["Message"] = ""
            elif event.unicode == '\x08' and console_data["Typing"]:#backspace
                handled_input = True
                console_data["Message"] = console_data["Message"][:-1]#undo

        if handled_input == False:
            non_global_inputs.append(event)

    if console_data["Command"] == "fps":
        console_data["Last Command"] = "fps"
        console_data["Command"] = ""
        console_data["FPS"] = not console_data["FPS"]

    if console_data["Command"] == "help":
        console_data["Last Command"] = "help"
        console_data["Command"] = ""
        log("fps - turn on/off fps display")

    return non_global_inputs

def draw_trans_rect(window, colour, trans, rect):
    s = pygame.Surface((rect[2],rect[3]))
    s.set_alpha(trans)
    s.fill(colour)
    window.blit(s, (rect[0], rect[1]))

def true_mouse_loc():
    false_loc = pygame.mouse.get_pos()
    real_loc = [false_loc[0], false_loc[1]]

    if (true_window.get_height() / true_window.get_width()) > (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen width
        bar_size = true_window.get_height() - (true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT)
        real_loc[1] -= (bar_size // 2)

        real_loc[0] = real_loc[0] / true_window.get_width() * WINDOW_WIDTH
        real_loc[1] = real_loc[1] / (true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT) * WINDOW_HEIGHT
        
    elif (true_window.get_height() / true_window.get_width()) <= (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen height
        bar_size = true_window.get_width() - (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH)
        real_loc[0] -= (bar_size // 2)   

        real_loc[1] = real_loc[1] / true_window.get_height() * WINDOW_HEIGHT    
        real_loc[0] = real_loc[0] / (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH) * WINDOW_WIDTH 
    
    return real_loc

def quit_game():
    pygame.quit()
    sys.exit()

### GAME CLASSES / FUNCTIONS

class Player:

    def __init__(self, loc = [1, 1]):
        self.loc = loc
        self.dir = random.choice(["U", "D", "L", "R"])
        self.new_floor = False

    def turn_left(self):
        if self.dir == "U":
            self.dir = "L"
        elif self.dir == "D":
            self.dir = "R"
        elif self.dir == "L":
            self.dir = "D"
        elif self.dir == "R":
            self.dir = "U"

    def turn_right(self):
        if self.dir == "U":
            self.dir = "R"
        elif self.dir == "D":
            self.dir = "L"
        elif self.dir == "L":
            self.dir = "U"
        elif self.dir == "R":
            self.dir = "D"

    def move(self, mov_dir, grid, flexit):
        cur_loc = copy.deepcopy(self.loc)
        if mov_dir == "w":
            if self.dir == "U":
                self.loc[1] -= 1
            elif self.dir == "D":
                self.loc[1] += 1
            elif self.dir == "L":
                self.loc[0] -= 1
            elif self.dir == "R":
                self.loc[0] += 1
        if mov_dir == "s":
            if self.dir == "U":
                self.loc[1] += 1
            elif self.dir == "D":
                self.loc[1] -= 1
            elif self.dir == "L":
                self.loc[0] += 1
            elif self.dir == "R":
                self.loc[0] -= 1
        if mov_dir == "a":
            if self.dir == "U":
                self.loc[0] -= 1
            elif self.dir == "D":
                self.loc[0] += 1
            elif self.dir == "L":
                self.loc[1] -= 1
            elif self.dir == "R":
                self.loc[1] += 1
        if mov_dir == "d":
            if self.dir == "U":
                self.loc[0] += 1
            elif self.dir == "D":
                self.loc[0] -= 1
            elif self.dir == "L":
                self.loc[1] += 1
            elif self.dir == "R":
                self.loc[1] -= 1

        if flexit == self.loc:
            self.new_floor = True
                
        if grid[self.loc[0]][self.loc[1]] == "#":
            self.loc = copy.deepcopy(cur_loc)

class Floor:

    def __init__(self):

        LV_GEN = "set"

        self.exit = [1, 0]

        if LV_GEN == "set":

            self.grid = [["#","#","#","#","#","#","#","#","#","#","#"],
                         ["#"," "," "," ","#","#","#"," "," "," ","#"],
                         ["#"," ","#"," "," "," "," "," ","#"," ","#"],
                         ["#"," "," ","#","#"," ","#","#"," "," ","#"],
                         ["#","#"," ","#","#"," ","#","#"," ","#","#"],
                         ["#","#"," "," "," "," "," "," "," ","#","#"],
                         ["#","#"," ","#","#"," ","#","#"," ","#","#"],
                         ["#"," "," ","#","#"," ","#","#"," "," ","#"],
                         ["#"," ","#"," "," "," "," "," ","#"," ","#"],
                         ["#"," "," "," ","#"," ","#"," "," "," ","#"],
                         ["#","#","#","#","#","#","#","#","#","#","#"]]

        if LV_GEN == "rand":

            MAX_SIZE = 11
            MAX_TUNNELS = 20
            MAX_LENGTH = 8

            self.grid = []

            for i in range(MAX_SIZE):
                self.grid.append([])
                for j in range(MAX_SIZE):
                    self.grid[-1].append("#")

            tunnel = [random.randint(1, MAX_SIZE - 2), random.randint(1, MAX_SIZE - 2)]

            for i in range(MAX_TUNNELS):
                tunnel_dir = random.choice([[0, 1], [1, 0], [0, -1], [-1, 0]])
                for j in range(random.randint(1, MAX_LENGTH)):
                    self.grid[tunnel[0]][tunnel[1]] = " "
                    tunnel = [tunnel[0] + tunnel_dir[0], tunnel[1] + tunnel_dir[1]]
                    if tunnel[0] == 0:
                        tunnel[0] = 1
                    if tunnel[0] == MAX_SIZE - 1:
                        tunnel[0] = MAX_SIZE - 2
                    if tunnel[1] == 0:
                        tunnel[1] = 1
                    if tunnel[1] == MAX_SIZE - 1:
                        tunnel[1] = MAX_SIZE - 2

        print(self.grid)

### MAIN FUNCTION

def main():

    options = ["START", "TUTORIAL"]

    game_state = "MAIN MENU"

    sel = 0
    count = 0
    mov = 0

    s_down = False
    w_down = False
    
    while True:
        
        count = 0
        mov = 0

        s_down = False
        w_down = False

        while game_state == "MAIN MENU": # the main menu
            clock.tick(FRAMERATE)

            count += 1
            if count >= FRAMERATE:
                count -= FRAMERATE

            junk = random.randint(0, 20)

            ## display

            game_window.fill((255, 255, 255))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 150)

            text = font.render("SILENT RIFT", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 20))

            pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH // 2 - text.get_width() // 2 - 5, 20 + text.get_height(), text.get_width() + 10, 20))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            for i in range(len(options)):

                tet = options[i]
                if sel == i:
                    tet = "> " + tet

                text = font.render(tet, True, (0, 0, 0))
                game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 350 + (i * 90) - text.get_height() // 2))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 80)

            text = font.render((PLAT_VER + " v." + DEV_VER), True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH - text.get_width() - 10, WINDOW_HEIGHT - text.get_height() - 10))

            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = options[sel]
                        log(("new game state: " + game_state))

                    if event.key == pygame.K_w and w_down == False:
                        w_down = True
                        mov -= 1
                        count = 15

                    if event.key == pygame.K_s and s_down == False:
                        s_down = True
                        mov += 1
                        count = 15

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_w and w_down == True:
                        w_down = False
                        mov += 1

                    if event.key == pygame.K_s and s_down == True:
                        s_down = False
                        mov -= 1

            if count == 15:
                count = 0
                sel += mov
                if sel < 0:
                    sel = len(options) - 1
                if sel > len(options) - 1:
                    sel = 0 

        while game_state == "TUTORIAL": # tutorial

            clock.tick(FRAMERATE)

            game_window.fill((255, 255, 255))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            text = font.render("TUTORIAL", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 20))

            pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH // 2 - text.get_width() // 2 - 5, 20 + text.get_height(), text.get_width() + 10, 20))

            game_window.blit(qr_code, (WINDOW_WIDTH // 2 - qr_code.get_width() // 2, 60 + text.get_height()))
     
            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                        log(("new game state: " + game_state))

        while game_state == "START": # the actual gameplay

            clock.tick(FRAMERATE)

            game_over = False

            floors_cleared = 0
            new_floor = True

            mov_dir = None
            mov_timer = 0

            en_mov_timer = 0

            dis_type = "REAL"

            while game_over == False:

                clock.tick(FRAMERATE)

                if mov_timer > 0:
                    mov_timer -= 1
                if en_mov_timer > 0:
                    en_mov_timer -= 1

                ## NEW FRAME

                if new_floor == True:
                    
                    new_display = True
                    new_floor = False
                    cur_floor = Floor()
                    loc = [1, 1]
                    player = Player(loc)
                    enemy = Enemy(velocity = 0, x = 9, y = 9, type = "Chaser")

                    print(player.loc)

                ## DISPLAY

                if new_display == True:
                    new_display = False

                    game_window.fill((255, 255, 255))

                    if dis_type == "FAKE":
                        temp_display(player, cur_floor, enemy)
                    elif dis_type == "REAL":
                        real_display(player, cur_floor, enemy)
         
                window_resize()

                ## INPUTS

                events = global_inputs()
                
                for event in events:
                    if event.type == pygame.KEYDOWN:
                                        
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            game_state = "MAIN MENU"
                            log(("new game state: " + game_state))

                        if event.key == pygame.K_w:
                            mov_dir = "w"
                        if event.key == pygame.K_a:
                            mov_dir = "a"
                        if event.key == pygame.K_s:
                            mov_dir = "s"
                        if event.key == pygame.K_d:
                            mov_dir = "d"
                        if event.key == pygame.K_e:
                            player.turn_right()
                        if event.key == pygame.K_q:
                            player.turn_left()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w and mov_dir == "w":
                            mov_dir = None
                        if event.key == pygame.K_a and mov_dir == "a":
                            mov_dir = None
                        if event.key == pygame.K_s and mov_dir == "s":
                            mov_dir = None
                        if event.key == pygame.K_d and mov_dir == "d":
                            mov_dir = None

                if console_data["Command"] == "dis":
                    console_data["Last Command"] = "dis"
                    console_data["Command"] = ""
                    if dis_type == "FAKE":
                        dis_type = "REAL"
                    else:
                        dis_type = "FAKE"

                ## ACTIONS

                # player mov

                if mov_dir != None and mov_timer == 0:
                    mov_timer = FRAMERATE / 4
                    player.move(mov_dir, cur_floor.grid, cur_floor.exit)
                    new_display = True

                if player.new_floor == True:
                    player.new_floor = False
                    new_floor = True

                else:

                    # enemy mov

                    if en_mov_timer == 0:
                        
                        new_display = True

                        en_mov_timer = 30

                        enemy.noticed_player(cur_floor.grid, player.loc, player.dir)
                        en_loc = enemy.ai_process(cur_floor.grid, player.loc)
                        enemy.x = en_loc[0]
                        enemy.y = en_loc[1]

                    if enemy.x == player.loc[0] and enemy.y == player.loc[1]: # player caught
                        game_over = True

            game_state = "GAME OVER"

        while game_state == "GAME OVER":

            clock.tick(FRAMERATE)

            game_window.fill((255, 255, 255))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            text = font.render("GAME OVER", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 20))

            pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH // 2 - text.get_width() // 2 - 5, 20 + text.get_height(), text.get_width() + 10, 20))
     
            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                        log(("new game state: " + game_state))

def temp_display(player, cur_floor, enemy):
    for x in range(0, len(cur_floor.grid)):
        for y in range(0, len(cur_floor.grid)):
            if cur_floor.grid[x][y] == "#":
                pygame.draw.rect(game_window, (0, 0, 0), (x*40, y*40, 40, 40))
            elif cur_floor.grid[x][y] == " ":
                pygame.draw.rect(game_window, (255, 255, 255), (x*40, y*40, 40, 40))

    pygame.draw.rect(game_window, (255, 255, 255), (cur_floor.exit[0]*40 + 10, cur_floor.exit[1]*40 + 10, 20, 20))

    pygame.draw.rect(game_window, (0, 255, 0), (player.loc[0]*40 + 10, player.loc[1]*40 + 10, 20, 20))
    
    pygame.draw.rect(game_window, (255, 0, 0), (enemy.x*40 + 10, enemy.y*40 + 10, 20, 20))

def real_display(player, cur_floor, enemy):
    #print(random.randint(0, 100))
    pygame.draw.rect(game_window, (154, 154, 154), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
    pygame.draw.rect(game_window, (158, 159, 125), (0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2))

    game_window.blit(test_img, (0, 0))

    surfaces = blurScreen(game_window)

    game_window.blit(surfaces[3], (0, 0))
    game_window.blit(surfaces[2], (WINDOW_WIDTH // 12, WINDOW_HEIGHT // 12))
    game_window.blit(surfaces[1], (WINDOW_WIDTH // 6, WINDOW_HEIGHT // 6))
    game_window.blit(surfaces[0], (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3))
                
# Create width and height constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
# Initialise all the pygame modules
pygame.init()
# Create a game window
true_window = pygame.display.set_mode((960, 720), pygame.RESIZABLE)
game_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set title
pygame.display.set_caption("Nario and Kuigi")
# PyGame Clock
clock = pygame.time.Clock()
# Blank Window
game_window.fill((255, 255, 255))
pygame.display.update()

console_log = []
console_data = {"Message": "",
                "Typing": False,
                "Command": "",
                "Last Command": "",
                "FPS": False}
    
PLAT_VER = "WIN"
DEV_VER = "DEV"
FRAMERATE = 60

if DEV_VER == "DEV":
    console_data["FPS"] = True
    
qr_code = pygame.image.load(resource_path("QR.png"))
test_img = pygame.image.load(resource_path("test.png"))
            
main()
