import random


class SnakeGame:
    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.snake_body = []
        self.food_position = None
        self.direction = "right"
        self.score = 0
        self.game_over = False

    def initialise_game(self, initial_length):
        initial_row = self.board_height // 2
        initial_col = self.board_width // 2
        self.snake_body = [
            (initial_row, initial_col - i) for i in range(initial_length)
        ]
        self.generate_food()

    def update_game_state(self):
        if not self.game_over:
            self.move_snake()
            self.check_collision()
            self.check_food_eaten()

    def move_snake(self):
        head_row, head_col = self.snake_body[0]
        if self.direction == "up":
            new_head = (head_row - 1, head_col)
        elif self.direction == "down":
            new_head = (head_row + 1, head_col)
        elif self.direction == "left":
            new_head = (head_row, head_col - 1)
        elif self.direction == "right":
            new_head = (head_row, head_col + 1)
        self.snake_body.insert(0, new_head)
        self.snake_body.pop()

    def check_collision(self):
        head_row, head_col = self.snake_body[0]
        if (
            head_row < 0
            or head_row >= self.board_height
            or head_col < 0
            or head_col >= self.board_width
        ):
            self.game_over = True
        elif self.snake_body[0] in self.snake_body[1:]:
            self.game_over = True

    def check_food_eaten(self):
        head = self.snake_body[0]
        if head == self.food_position:
            self.score += 10
            self.grow_snake()
            self.generate_food()

    def generate_food(self):
        all_positions = [
            (row, col)
            for row in range(self.board_height)
            for col in range(self.board_width)
        ]
        available_positions = [
            pos for pos in all_positions if pos not in self.snake_body
        ]
        self.food_position = random.choice(available_positions)

    def grow_snake(self):
        tail = self.snake_body[-1]
        self.snake_body.append(tail)

    def change_direction(self, new_direction):
        opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
