from tkinter import *
import random 

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SNAKE_SPEED = 200
BOX_SIZE = 20
SNAKE_SIZE = 3
COLOR_SNAKE = "#00FF00"
COLOR_FOOD = "red"
COLOR_BACKGROUND = "#000000"

score = 0
direction = 'down'

canvas = None  
window = None  
label = None  
label_length_of_body = None 

class Organism:
    def __init__(self): 
        self.size = SNAKE_SIZE
        self.coordinates = [] 
        self.blocks = []
		 
        for i in range(0, SNAKE_SIZE): 
            self.coordinates.append([0, 0])

        for x, y in self.coordinates: 
            block = canvas.create_rectangle(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=COLOR_SNAKE, tag="organism") 
            self.blocks.append(block)

class Meal:
    def __init__(self): 
        x = random.randint(0, (SCREEN_WIDTH / BOX_SIZE) - 1) * BOX_SIZE 
        y = random.randint(0, (SCREEN_HEIGHT / BOX_SIZE) - 1) * BOX_SIZE 
        self.coordinates = [x, y]          
        canvas.create_oval(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=COLOR_FOOD, tag="food") 

def Initialize_window(window):
    window.title("Snake game") 
    window.update() 

    window_width = window.winfo_width() 
    window_height = window.winfo_height() 
    screen_width = window.winfo_screenwidth() 
    screen_height = window.winfo_screenheight() 

    x = int((screen_width/2) - (window_width/2)) 
    y = int((screen_height/2) - (window_height/2)) 

    window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

def next_turn(snake, food): 
    x, y = snake.coordinates[0]

    if direction == "up": 
        y -= BOX_SIZE 
    elif direction == "down": 
        y += BOX_SIZE 
    elif direction == "left": 
        x -= BOX_SIZE 
    elif direction == "right": 
        x += BOX_SIZE 

    snake.coordinates.insert(0, (x, y)) 

    block = canvas.create_rectangle(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=COLOR_SNAKE) 
    snake.blocks.insert(0, block) 

    if x == food.coordinates[0] and y == food.coordinates[1]: 
        global score 
        score += 1

        label.config(text="Points:{}".format(score)) 
        label_length_of_body.config(text="Length of Snake:{}".format(score + 3)) 

        canvas.delete("food") 
        food = Meal() 
    else: 
        del snake.coordinates[-1] 
        canvas.delete(snake.blocks[-1]) 
        del snake.blocks[-1] 

    if check_collisions(snake): 
        game_over() 
    else: 
        window.after(SNAKE_SPEED, next_turn, snake, food) 

def change_direction(new_direction): 
    global direction 

    if new_direction == 'left' and direction != 'right': 
        direction = new_direction 
    elif new_direction == 'right' and direction != 'left': 
        direction = new_direction 
    elif new_direction == 'up' and direction != 'down': 
        direction = new_direction 
    elif new_direction == 'down' and direction != 'up': 
        direction = new_direction 

def check_collisions(snake): 
    x, y = snake.coordinates[0] 
    if x < 0 or x >= SCREEN_WIDTH: 
        return True
    elif y < 0 or y >= SCREEN_HEIGHT: 
        return True
    for body_part in snake.coordinates[1:]: 
        if x == body_part[0] and y == body_part[1]: 
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    restart_button = Button(window, text="Restart", command=restart_game)
    restart_button.pack(pady=20)

def restart_game():
    global score, direction, snake, food
    score = 0
    direction = 'down'

    canvas.delete("all")
    snake = Organism()
    food = Meal()

    label.config(text="Points:{}".format(score))
    label.pack()
    label_length_of_body.config(text="Length of Snake:{}".format(score + 3))

    next_turn(snake, food)

def main():
    global window, canvas, label, label_length_of_body
    window = Tk()

    label = Label(window, text="Points:{}".format(score), font=('Comic Sans', 20)) 
    label.pack() 

    label_length_of_body = Label(window, text="Length of Snake:{}".format(score + 3), font=('Comic Sans', 20)) 
    label_length_of_body.pack() 

    canvas = Canvas(window, bg=COLOR_BACKGROUND, height=SCREEN_HEIGHT, width=SCREEN_WIDTH) 
    canvas.pack()

    Initialize_window(window)

    window.bind("<KeyPress>", change_direction)
    window.bind('<Left>', lambda event: change_direction('left')) 
    window.bind('<Right>', lambda event: change_direction('right')) 
    window.bind('<Up>', lambda event: change_direction('up')) 
    window.bind('<Down>', lambda event: change_direction('down')) 

    snake = Organism() 
    food = Meal() 

    next_turn(snake, food) 

    window.mainloop() 

if __name__ == "__main__":
    main()
