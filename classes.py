# Snake
import random

class Snake:
    def __init__(self, body: list, direction: tuple):
        self.body = body
        self.direction = direction

    def take_step(self, position: tuple, remove: bool):
        if remove:
            self.body.pop(0)
        self.body.append(position)

    def set_direction(self, direction: tuple):
        self.direction = direction

    def get_next_step(self) -> tuple:
        add_x, add_y = self.direction
        x, y = (self.body[-1][0], self.body[-1][1])
        x += add_x
        y += add_y
        return (x, y)

    def get_head(self) -> tuple:
        return self.body[-1]

    def __str__(self):
        return f"Body: {self.body} , direction: {self.direction}"


class Apple:
    def __init__(self, height, width):
        self.set_random_position(height, width)

    def set_random_position(self, height, width):
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        self.position = (x, y)

class Game:
    def __init__(self, height: int, width: int, snake_body: list, snake_direction: tuple):
        if height <= 0 or width <= 0:
            raise ValueError("Height and width must be positive")
        self.height = height
        self.width = width
        self.snake = Snake(snake_body, snake_direction)
        self.apple = Apple(height, width)
        self.score = 0

    def board_matrix(self) -> list:
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def render_box_row(self, len_row: int) -> str:
        rendered_matrix = ""
        rendered_matrix += "+"
        rendered_matrix += "-" * len_row
        rendered_matrix += "+"
        return rendered_matrix

    def update_if_out_of_bounds(self, next_step: tuple) -> tuple:
        if next_step[0] == self.height:
            next_step = (0, next_step[1])
        if next_step[0] < 0:
            next_step = (self.height - 1, next_step[1])
        if next_step[1] == self.width:
            next_step = (next_step[0], 0)
        if next_step[1] < 0:
            next_step = (next_step[0], self.width - 1)
        return next_step

    def render(self) -> None:
        # Get board
        matrix = self.board_matrix()

        # Set the snakes body
        for x, y in self.snake.body:
            matrix[x][y] = "O"
        # Set the snakes head
        x, y = self.snake.get_head()
        matrix[x][y] = "X"

        x, y = self.apple.position
        matrix[x][y] = "*"

        self.render_terminal(matrix)

    def render_terminal(self, matrix) -> None:

        # Render box
        rendered_matrix = ""
        rendered_matrix += self.render_box_row(len(matrix[0]))

        # Render rows
        for row in matrix:
            rendered_matrix += "\n|"

            # Render content
            for field in row:
                # Empty field
                if field is None:
                    rendered_matrix += " "
                # Everything else
                else:
                    rendered_matrix += field

            rendered_matrix += "|"

        # Render box
        rendered_matrix += "\n"
        rendered_matrix += self.render_box_row(len(matrix[0]))

        # Print rendered matrix
        print(rendered_matrix)
