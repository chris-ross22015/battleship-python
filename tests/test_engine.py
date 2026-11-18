from battleship.engine import GameEngine


def test_board_dimensions():
    engine = GameEngine(grid_size=6, ship_sizes=[3,2], max_shots=10)
    assert len(engine.board) == 6
    assert all(len(row) == 6 for row in engine.board)

def test_ship_placement_total_cells():
    ship_sizes = [4, 3, 2]
    engine = GameEngine(grid_size=8, ship_sizes=ship_sizes, max_shots=20)

    placed_cells = sum(cell == 1 for row in engine.board for cell in row)
    assert placed_cells == sum(ship_sizes)

def test_fire_shot_hit_and_miss():
    engine = GameEngine(grid_size=4, ship_sizes=[2], max_shots=5)
    engine.board = engine.create_board()
    engine.board[0][0] = 1
    engine.board[0][1] = 1

    hit_result = engine.fire_shot(0, 0)
    assert hit_result == "hit"
    assert engine.hits == 1
    assert engine.shots_left == 4
    assert engine.game_over is False

    miss_result = engine.fire_shot(3, 3)
    assert miss_result == "miss"
    assert engine.hits == 1
    assert engine.shots_left == 3
    assert engine.game_over is False

def test_victory_condition():
    engine = GameEngine(grid_size=4, ship_sizes=[1], max_shots=5)
    engine.board = engine.create_board()
    engine.board[1][1] = 1

    result = engine.fire_shot(1, 1)
    assert result == "hit"
    assert engine.game_over is True
    assert engine.won is True
    assert engine.fire_shot(0, 0) == "ignored"

def test_out_of_ammo_loss_condition():
    engine = GameEngine(grid_size=4, ship_sizes=[2], max_shots=1)
    engine.board = engine.create_board()
    engine.board[0][0] = 1
    engine.board[0][1] = 1

    result = engine.fire_shot(3, 3)

    assert result == "miss"
    assert engine.shots_left == 0
    assert engine.game_over is True
    assert engine.won is False
