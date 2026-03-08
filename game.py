import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 700
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Fruit Eater')

clock = pygame.time.Clock()

snake_block = 15
food_size = 30

font_style = pygame.font.SysFont("ARCADECLASSIC", 28)
menu_font = pygame.font.SysFont("centurygothic", 35)
score_font = pygame.font.SysFont("agencyfb", 35)

background = pygame.image.load("img.jpg").convert()
interface_background = pygame.image.load("snakei.jpg").convert()
red_food_image = pygame.image.load("bomb.png").convert_alpha()
red_food_image = pygame.transform.scale(red_food_image, (food_size, food_size))
blue_food_image = pygame.image.load("red_transparent.png").convert_alpha()
blue_food_image = pygame.transform.scale(blue_food_image, (food_size, food_size))

high_score = 0
user_scores = {}  

apple_bite_sound = pygame.mixer.Sound("eating.mp3")
game_over_sound = pygame.mixer.Sound("gameover.mp3")

def Your_score(score, high_score, username=None):
    value = score_font.render("Your Score: " + str(score), True, black)
    high_score_value = score_font.render("High Score: " + str(high_score), True, black)
    dis.blit(value, [10, 10])
    dis.blit(high_score_value, [dis_width - 160, 10])
    if username:
        username_value = score_font.render("Username: " + username, True, black)
        dis.blit(username_value, [10, 50])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displacement=0, font=None):
    if font is None:
        font = font_style
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 + y_displacement])

def get_username():
    username = ""
    input_box = pygame.Rect(dis_width / 2 - 70, dis_height / 2 + 40, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    while True:
        dis.fill((30, 30, 30))
        prompt = font.render("Enter Player Name", True, white)
        dis.blit(prompt, (dis_width / 2 - prompt.get_width() / 2, dis_height / 2 - 40))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        dis.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(dis, color, input_box, 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width()+10)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

def gameLoop(username):
    global high_score, user_scores

    game_over = False
    game_close = False
    new_high_score = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    snake_speed = 10

    foodx = round(random.randrange(0, dis_width - food_size) / 15.0) * 15.0
    foody = round(random.randrange(0, dis_height - food_size) / 15.0) * 15.0

    red_foodx = round(random.randrange(0, dis_width - food_size) / 15.0) * 15.0
    red_foody = round(random.randrange(0, dis_height - food_size) / 15.0) * 15.0

    while not game_over:

        while game_close:
            dis.blit(background, [0, 0])
            message("Press W to play again M to return to Menu Q to Quit", red, y_displacement=-80)
            message(f"Your Score  {Length_of_snake - 1}", black)
            message(f"High Score  {high_score}", black, y_displacement=50)

            if new_high_score:
                message("New High Score", black, y_displacement=100)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_w:
                        user_scores[username] = Length_of_snake - 1
                        gameLoop(username)
                    elif event.key == pygame.K_m:
                        user_scores[username] = Length_of_snake - 1
                        start_menu()
                    elif event.key == pygame.K_d:
                        user_scores[username] = Length_of_snake - 1
                        show_dashboard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            game_over_sound.play() 

        x1 += x1_change
        y1 += y1_change
        dis.blit(background, [0, 0])

        dis.blit(blue_food_image, [foodx, foody])
        dis.blit(red_food_image, [red_foodx, red_foody])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                game_over_sound.play()  

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1, high_score, username)

        pygame.display.update()

        if abs(x1 - foodx) < food_size and abs(y1 - foody) < food_size:
            apple_bite_sound.play() 
            foodx = round(random.randrange(0, dis_width - food_size) / 15.0) * 15.0
            foody = round(random.randrange(0, dis_height - food_size) / 15.0) * 15.0
            Length_of_snake += 1
            snake_speed += 1

            if Length_of_snake - 1 > high_score:
                high_score = Length_of_snake - 1
                new_high_score = True

            red_foodx = round(random.randrange(0, dis_width - food_size) / 15.0) * 15.0
            red_foody = round(random.randrange(0, dis_height - food_size) / 15.0) * 15.0

        if abs(x1 - red_foodx) < food_size and abs(y1 - red_foody) < food_size:
            game_close = True
            game_over_sound.play() 

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def show_dashboard():
    global user_scores

    dashboard_background = pygame.image.load("snui7.jpg").convert()
    dashboard_background = pygame.transform.scale(dashboard_background, (dis_width, dis_height))

    dis.blit(dashboard_background, [0, 0]) 
    y_offset = -200

    sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)


    for user, score in sorted_scores:
        message(f"{user}: {score}", white, y_displacement=y_offset, font=score_font)
        y_offset += 50


    back_text = score_font.render("Press B to go back", True, white)
    dis.blit(back_text, [dis_width / 2 - back_text.get_width() / 2, dis_height - 50])

    pygame.display.update()


    waiting_for_back = True
    while waiting_for_back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    start_menu() 
                    waiting_for_back = False

    

def start_menu():
    global high_score
    username = ""
    while True:
        dis.blit(interface_background, [0, 0])
        title = menu_font.render("Fruit Eater", True, black)
        start_button = menu_font.render("Press Space to Start", True, black)
        instructions_button = menu_font.render("Press I for Instructions", True, black)
        new_user_button = menu_font.render("Press N for New User", True, black)
        dashboard_button = menu_font.render("Press D for Dashboard", True, black)

        dis.blit(title, [dis_width / 2 - title.get_width() / 2, dis_height / 2 - 200])
        dis.blit(start_button, [dis_width / 2 - start_button.get_width() / 2, dis_height / 2 - 50])
        dis.blit(instructions_button, [dis_width / 2 - instructions_button.get_width() / 2, dis_height / 2])
        dis.blit(new_user_button, [dis_width / 2 - new_user_button.get_width() / 2, dis_height / 2 + 50])
        dis.blit(dashboard_button, [dis_width / 2 - dashboard_button.get_width() / 2, dis_height / 2 + 100])
        
        team_names = ["Deepak Shyam Vessley K", "Harish B", "Syed Kazi Ahamed Hussain S"]
        team_font = pygame.font.SysFont("centurygothic", 20)
        y_offset = dis_height - 100
        for name in team_names:
            name_surface = team_font.render(name, True, black)
            dis.blit(name_surface, [dis_width - name_surface.get_width() - 70, y_offset])
            y_offset += 25 

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if username == "":
                        username = get_username()
                    gameLoop(username)
                elif event.key == pygame.K_i:
                    instructions()
                elif event.key == pygame.K_n:
                    username = get_username()
                elif event.key == pygame.K_d:
                    show_dashboard()

def instructions():
    dis.blit(background, [0, 0])
    message("Use Arrow Keys to Move", black, y_displacement=-50)
    message("Eat the apple to Grow", black, y_displacement=-30)
    message("Avoid the bomb and dont hit the edges", black, y_displacement=0)
    message("Press Q to Quit", black, y_displacement=40)
    message("Press Space to Start", black, y_displacement=70)
    pygame.display.update()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

start_menu()
