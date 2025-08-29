# Test Snake
from classes import Apple, Game, Snake

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)

def test_board_matrix():
    game = Game(1, 1, [(0, 0), (0, 1)], DOWN)
    assert game.board_matrix() == [[None]]

    game = Game(2, 2, [(0, 0), (0, 1)], DOWN)
    assert game.board_matrix() == [[None, None], [None, None]]

    game = Game(1, 2, [(0, 0), (0, 1)], DOWN)
    assert game.board_matrix() == [[None, None]]

    game = Game(3, 1, [(0, 0), (0, 1)], DOWN)
    assert game.board_matrix() == [[None], [None], [None]]
