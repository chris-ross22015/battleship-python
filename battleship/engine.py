import random

try:
    from battleship import config
except ImportError:
    import config

class GameEngine:
    def __init__(self, grid_size=config.GRID_SIZE, ship_sizes=config.SHIP_SIZES, max_shots=config.MAX_SHOTS):
        self.grid_size = grid_size
        self.ship_sizes = ship_sizes
        self.max_shots = max_shots
        self.board = self.create_board()
        self.place_ships()
        self.shots_left = self.max_shots
        self.hits = 0
        self.total_ship_cells = sum(self.ship_sizes)
        self.game_over = False
        self.won = False

    def create_board(self):
        return [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def place_ships(self):
        for size in self.ship_sizes:
            while True:
                orientation = random.choice(["hrztl", "vert"])
                if orientation == "hrztl":
                    start_r = random.randint(0, self.grid_size - 1)
                    start_c = random.randint(0, self.grid_size - size)
                    ship_coords = [(start_r, start_c + i) for i in range(size)]
                elif orientation == "vert":
                    start_r = random.randint(0, self.grid_size - size)
                    start_c = random.randint(0, self.grid_size - 1)
                    ship_coords = [(start_r + i, start_c) for i in range(size)]
                if all(self.board[r][c] == 0 for r, c in ship_coords):
                    for r, c in ship_coords:
                        self.board[r][c] = 1
                    break
    
    def fire_shot(self, r, c):
        if self.game_over:
            return "ignored"

        is_hit = self.board[r][c] == 1
        if is_hit:
            self.hits += 1
        self.shots_left -= 1

        if self.hits == self.total_ship_cells:
            self.game_over = True
            self.won = True
        elif self.shots_left == 0:
            self.game_over = True
            self.won = False
        return "hit" if is_hit else "miss"