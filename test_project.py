# Test Snake
import pytest
from classes import Game

DOWN = (1, 0)

@pytest.mark.parametrize(
    "height,width,expected",
    [
        (1, 1, [[None]]),
        (2, 2, [[None, None], [None, None]]),
        (1, 2, [[None, None]]),
        (3, 1, [[None], [None], [None]]),
    ],
)
def test_board_matrix(height, width, expected):
    game = Game(height, width, [(0, 0), (0, 1)], DOWN)
    assert game.board_matrix() == expected


@pytest.mark.parametrize(
    "next_step,expected",
    [
        ((10, 0), (0, 0)),
        ((-1, 0), (9, 0)),
        ((0, 20), (0, 0)),
        ((0, -1), (0, 19)),
    ],
)
def test_update_if_out_of_bounds(next_step, expected):
    game = Game(10, 20, [(0, 0)], DOWN)
    assert game.update_if_out_of_bounds(next_step) == expected


def test_invalid_dimensions():
    with pytest.raises(ValueError):
        Game(0, 1, [(0, 0)], DOWN)
    with pytest.raises(ValueError):
        Game(1, 0, [(0, 0)], DOWN)
