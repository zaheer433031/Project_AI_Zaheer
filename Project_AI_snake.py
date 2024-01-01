from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500

SNAKE_SPEED = 200
BOX_SIZE = 20
SNAKE_SIZE = 3
SNAKE_COLOR = "#00FF00"
AI_SNAKE_COLOR = "#800080"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "#000000"

human_score = 0
ai_score = 0

label_human = None
label_ai = None

direction = 'down'
canvas = None
window = None


class Snake:
    def __init__(self, color):
        self.size = SNAKE_SIZE
        self.coordinates = []
        self.squares = []
        self.color = color

        for i in range(0, SNAKE_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / BOX_SIZE) - 1) * BOX_SIZE
        y = random.randint(0, (GAME_HEIGHT / BOX_SIZE) - 1) * BOX_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=FOOD_COLOR, tag="food")


def initialize_window(window):
    window.title("Snake game")
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def next_turn(snake, ai_snake, food):
    global SNAKE_SPEED

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

    square = canvas.create_rectangle(x, y, x + BOX_SIZE, y + BOX_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    ai_direction = get_ai_direction(ai_snake.coordinates, food.coordinates)
    x_ai, y_ai = ai_snake.coordinates[0]

    if ai_direction == "up":
        y_ai -= BOX_SIZE
    elif ai_direction == "down":
        y_ai += BOX_SIZE
    elif ai_direction == "left":
        x_ai -= BOX_SIZE
    elif ai_direction == "right":
        x_ai += BOX_SIZE

    ai_snake.coordinates.insert(0, (x_ai, y_ai))

    square = canvas.create_rectangle(x_ai, y_ai, x_ai + BOX_SIZE, y_ai + BOX_SIZE, fill=AI_SNAKE_COLOR)
    ai_snake.squares.insert(0, square)

    print("Human Snake Head:", x, y)
    print("AI Snake Head:", x_ai, y_ai)
    print("Food Coordinates:", food.coordinates)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global human_score
        human_score += 1

        label_human.config(text="Human Score:{}".format(human_score))

        canvas.delete("food")
        food = Food()

        del ai_snake.coordinates[-1]
        canvas.delete(ai_snake.squares[-1])
        del ai_snake.squares[-1]

    elif x_ai == food.coordinates[0] and y_ai == food.coordinates[1]:
        global ai_score
        ai_score += 1

        label_ai.config(text="AI Score:{}".format(ai_score))

        canvas.delete("food")
        food = Food()

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

        del ai_snake.coordinates[-1]
        canvas.delete(ai_snake.squares[-1])
        del ai_snake.squares[-1]

    if check_collisions(snake) or check_collisions(ai_snake):
        game_over()
    else:
        window.after(SNAKE_SPEED, next_turn, snake, ai_snake, food)


def get_ai_direction(ai_coordinates, food_coordinates):
    ai_x, ai_y = ai_coordinates[0]
    food_x, food_y = food_coordinates

    if ai_x < food_x:
        return "right"
    elif ai_x > food_x:
        return "left"
    elif ai_y < food_y:
        return "down"
    elif ai_y > food_y:
        return "up"


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

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    # Adding a button to restart game
    restart_button = Button(window, text="Restart", command=restart_game)
    restart_button.pack(pady=20)


def restart_game():
    global human_score, ai_score, direction, snake, ai_snake, food
    human_score = 0
    ai_score = 0
    direction = 'down'

    canvas.delete("all")
    snake = Snake(SNAKE_COLOR)
    ai_snake = Snake(AI_SNAKE_COLOR)
    food = Food()

    label_human.config(text="Human Score:{}".format(human_score))
    label_ai.config(text="AI Score:{}".format(ai_score))
    label_human.pack()
    label_ai.pack()

    next_turn(snake, ai_snake, food)


def main():
    global window, canvas, label_human, label_ai, snake, ai_snake, food
    window = Tk()

    label_human = Label(window, text="Human Score:{}".format(human_score), font=('Comic Sans', 20))
    label_human.pack()

    label_ai = Label(window, text="AI Score:{}".format(ai_score), font=('Comic Sans', 20))
    label_ai.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    initialize_window(window)

    window.bind("<KeyPress>", change_direction)
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    snake = Snake(SNAKE_COLOR)
    ai_snake = Snake(AI_SNAKE_COLOR)
    food = Food()

    next_turn(snake, ai_snake, food)

    window.mainloop()


if __name__ == "__main__":
    main()
