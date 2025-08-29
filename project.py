from classes import Game

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)

VALID_MOVES = {
    "u": UP,
    "d": DOWN,
    "l": LEFT,
    "r": RIGHT,
}

snake_init_body = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
game = Game(10, 20, snake_init_body, DOWN)

while True:
    game.render()
    direction = input("Direction: ")
    #direction = "u"
    if direction in VALID_MOVES:
        game.snake.set_direction(VALID_MOVES[direction])
    next_step = game.snake.get_next_step()

# Check out of bounds
    next_step = game.update_if_out_of_bounds(next_step)

    # Check if next_step kills us
    if next_step in game.snake.body[1:]:
        break

    # Check if next step is apple
    if next_step == game.apple.position:
        game.score += 1
        game.apple.set_random_position(game.height, game.width)
        game.snake.take_step(next_step, False)
    else:
        game.snake.take_step(next_step, True)

print("GAME OVER!")
print(f"Score: {game.score}")
