from battleship.engine import GameEngine


def test_board_dimensions():
    engine = GameEngine(grid_size=6, ship_sizes=[3, 2], max_shots=10)
    assert len(engine.board) == 6 and all(len(row) == 6 for row in engine.board)


def test_ship_placement_total_cells():
    ship_sizes = [4, 3, 2]
    engine = GameEngine(grid_size=8, ship_sizes=ship_sizes, max_shots=20)
    assert sum(cell == 1 for row in engine.board for cell in row) == sum(ship_sizes)
    assert len(engine.ships) == len(ship_sizes)
    assert engine.player_hp == sum(ship_sizes) and engine.max_player_hp == sum(ship_sizes)


def test_fire_shot_hit_sunk_and_miss():
    engine = GameEngine(grid_size=4, ship_sizes=[2, 1], max_shots=5)
    engine.board = engine.create_board()
    engine.board[0][0], engine.board[0][1], engine.board[2][2] = 1, 1, 1
    engine.ships = [{(0, 0), (0, 1)}, {(2, 2)}]

    assert engine.fire_shot(0, 0) == "hit" and engine.hits == 1 and engine.shots_left == 4 and not engine.game_over
    assert engine.fire_shot(3, 3) == "miss" and engine.hits == 1 and engine.shots_left == 3 and not engine.game_over
    assert engine.fire_shot(0, 1) == "sunk" and engine.hits == 2 and engine.shots_left == 2 and not engine.game_over


def test_victory_condition():
    engine = GameEngine(grid_size=4, ship_sizes=[1], max_shots=5)
    engine.board = engine.create_board()
    engine.board[1][1] = 1
    engine.ships = [{(1, 1)}]

    assert engine.fire_shot(1, 1) == "sunk"
    assert engine.game_over is True and engine.won is True and engine.player_hp == 1
    assert engine.fire_shot(0, 0) == "ignored"


def test_out_of_ammo_loss_condition():
    engine = GameEngine(grid_size=4, ship_sizes=[2], max_shots=1)
    engine.board = engine.create_board()
    engine.board[0][0], engine.board[0][1] = 1, 1
    engine.ships = [{(0, 0), (0, 1)}]

    assert engine.fire_shot(3, 3) == "miss"
    assert engine.shots_left == 0 and engine.game_over is True and engine.won is False and engine.loss_reason == "ammo"


def test_player_hp_zero_loss_condition():
    engine = GameEngine(grid_size=4, ship_sizes=[2], max_shots=10)
    engine.place_player_ship(0, 0, 2, "hrztl")

    for _ in range(16):
        if engine.game_over:
            break
        engine.execute_ai_turn()

    assert engine.player_hp == 0 and engine.game_over is True and engine.won is False and engine.loss_reason == "hp"


def test_player_ship_placement_valid():
    engine = GameEngine(grid_size=10, ship_sizes=[4, 3, 2])
    assert engine.place_player_ship(0, 0, 4, "hrztl") is True
    assert len(engine.player_ships) == 1 and engine.player_board[0][0:4] == [1, 1, 1, 1]


def test_player_ship_placement_out_of_bounds():
    engine = GameEngine(grid_size=10, ship_sizes=[4, 3, 2])
    assert engine.place_player_ship(0, 8, 4, "hrztl") is False
    assert engine.place_player_ship(8, 0, 4, "vert") is False
    assert len(engine.player_ships) == 0


def test_player_ship_placement_overlap_rejected():
    engine = GameEngine(grid_size=10, ship_sizes=[4, 3, 2])
    assert engine.place_player_ship(2, 2, 3, "hrztl") is True
    assert engine.place_player_ship(1, 3, 3, "vert") is False
    assert len(engine.player_ships) == 1 and engine.player_board[1][3] == 0


def test_player_shots_tracking():
    engine = GameEngine(grid_size=6, ship_sizes=[2], max_shots=10)
    (r1, c1), (r2, c2) = list(engine.ships[0])

    assert engine.fire_shot(r1, c1) == "hit" and engine.player_shots[(r1, c1)] == "hit"
    assert engine.fire_shot(r1, c1) == "ignored"
    assert engine.fire_shot(r2, c2) == "sunk"
    assert engine.player_shots[(r1, c1)] == "sunk" and engine.player_shots[(r2, c2)] == "sunk"


def test_execute_ai_turn_tracks_shots_and_sinks():
    engine = GameEngine(grid_size=4, ship_sizes=[2], max_shots=10)
    engine.place_player_ship(0, 0, 2, "hrztl")

    for _ in range(16):
        if engine.game_over:
            break
        result = engine.execute_ai_turn()
        assert result in ("hit", "miss", "sunk") and engine.last_ai_shot in engine.ai_shots

    assert engine.player_hp == 0 and engine.game_over is True and engine.loss_reason == "hp"
    assert engine.ai_shots[(0, 0)] == "sunk" and engine.ai_shots[(0, 1)] == "sunk"