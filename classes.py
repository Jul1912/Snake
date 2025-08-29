"""Core classes for the terminal-based Snake game."""

import random


class Snake:
    """Model the snake's body and movement state."""

    def __init__(self, body: list, direction: tuple):
        """Initialize a snake instance.

        Args:
            body (list[tuple[int, int]]):
                Ordered coordinates representing the snake from tail to head.
            direction (tuple[int, int]):
                Movement vector describing the current heading.
        """
        self.body = body
        self.direction = direction

    def take_step(self, position: tuple, remove: bool):
        """Move the snake forward by one step.

        Args:
            position (tuple[int, int]): New head position.
            remove (bool): Whether to remove the tail segment
                (``True`` during normal movement, ``False`` when growing).
        """
        if remove:
            self.body.pop(0)
        self.body.append(position)

    def set_direction(self, direction: tuple):
        """Update the snake's movement direction.

        Args:
            direction (tuple[int, int]): Movement vector for subsequent steps.
        """
        self.direction = direction

    def get_next_step(self) -> tuple:
        """Compute the coordinates of the next head position.

        Returns:
            tuple[int, int]: Position resulting from applying the current direction.
        """
        add_x, add_y = self.direction
        x, y = (self.body[-1][0], self.body[-1][1])
        x += add_x
        y += add_y
        return (x, y)

    def get_head(self) -> tuple:
        """Return the current head position."""
        return self.body[-1]

    def __str__(self):
        """Return a string representation of the snake."""
        return f"Body: {self.body} , direction: {self.direction}"


class Apple:
    """Represent an apple that spawns at random board positions."""

    def __init__(self, height, width):
        """Create an apple at a random position within the board.

        Args:
            height (int): Board height.
            width (int): Board width.
        """
        self.set_random_position(height, width)

    def set_random_position(self, height, width):
        """Place the apple at a random coordinate on the board.

        Args:
            height (int): Board height.
            width (int): Board width.
        """
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        self.position = (x, y)


class Game:
    """Coordinate the Snake game, handling state and rendering."""

    def __init__(self, height: int, width: int, snake_body: list, snake_direction: tuple):
        """Initialize the game with board size and initial snake configuration.

        Args:
            height (int): Number of rows on the board.
            width (int): Number of columns on the board.
            snake_body (list[tuple[int, int]]): Initial positions of the snake.
            snake_direction (tuple[int, int]): Initial movement direction.

        Raises:
            ValueError: If ``height`` or ``width`` is not positive.
        """
        if height <= 0 or width <= 0:
            raise ValueError("Height and width must be positive")
        self.height = height
        self.width = width
        self.snake = Snake(snake_body, snake_direction)
        self.apple = Apple(height, width)
        self.score = 0

    def board_matrix(self) -> list:
        """Return an empty board matrix sized according to the game dimensions.

        Returns:
            list[list[None]]: Matrix initialized with ``None`` values.
        """
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def render_box_row(self, len_row: int) -> str:
        """Create a horizontal border string for rendering the board.

        Args:
            len_row (int): Width of the board.

        Returns:
            str: String containing the border representation.
        """
        rendered_matrix = ""
        rendered_matrix += "+"
        rendered_matrix += "-" * len_row
        rendered_matrix += "+"
        return rendered_matrix

    def update_if_out_of_bounds(self, next_step: tuple) -> tuple:
        """Wrap the snake around if the next step is outside the board.

        Args:
            next_step (tuple[int, int]): Proposed head position.

        Returns:
            tuple[int, int]: Adjusted position within board bounds.
        """
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
        """Render the current game state to the terminal."""
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
        """Print a visual representation of the board to the terminal.

        Args:
            matrix (list[list[str | None]]): Board to render.
        """

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
