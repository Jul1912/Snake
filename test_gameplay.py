import pytest
import random
from classes import Game, Apple

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)


@pytest.fixture
def game():
    # Simple game with snake facing down
    body = [(0, 0), (0, 1), (0, 2)]
    return Game(5, 5, body, DOWN)


def test_take_step_moves_snake(game):
    next_step = game.snake.get_next_step()
    game.snake.take_step(next_step, True)
    assert game.snake.body == [(0, 1), (0, 2), (1, 2)]


def test_take_step_grows_snake(game):
    next_step = game.snake.get_next_step()
    game.snake.take_step(next_step, False)
    assert game.snake.body == [(0, 0), (0, 1), (0, 2), (1, 2)]


@pytest.mark.parametrize(
    "next_step,expected",
    [
        ((5, 2), (0, 2)),
        ((-1, 2), (4, 2)),
        ((2, 5), (2, 0)),
        ((2, -1), (2, 4)),
    ],
)
def test_update_if_out_of_bounds_wraps(next_step, expected, game):
    assert game.update_if_out_of_bounds(next_step) == expected


def test_apple_placement_within_bounds(monkeypatch):
    # force apple position to (0, 0)
    monkeypatch.setattr(random, "randint", lambda a, b: 0)
    apple = Apple(3, 3)
    assert apple.position == (0, 0)
    # move apple again to ensure still within bounds
    apple.set_random_position(3, 3)
    assert apple.position == (0, 0)


@pytest.fixture
def collision_game():
    body = [(1, 1), (1, 2), (2, 2), (2, 1)]
    return Game(4, 4, body, LEFT)


def test_collision_with_self_detected(collision_game):
    next_step = collision_game.snake.get_next_step()
    next_step = collision_game.update_if_out_of_bounds(next_step)
    assert next_step in collision_game.snake.body[1:]


def test_scoring_and_growth_on_apple(monkeypatch, game):
    game.apple.position = (1, 2)

    def fixed_position(height, width):
        game.apple.position = (0, 0)

    monkeypatch.setattr(game.apple, "set_random_position", fixed_position)

    next_step = game.snake.get_next_step()
    next_step = game.update_if_out_of_bounds(next_step)

    if next_step == game.apple.position:
        game.score += 1
        game.apple.set_random_position(game.height, game.width)
        game.snake.take_step(next_step, False)
    else:
        game.snake.take_step(next_step, True)

    assert game.score == 1
    assert len(game.snake.body) == 4
    assert game.apple.position == (0, 0)
