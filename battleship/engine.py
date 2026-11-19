import random

try:
    from battleship import config
except ImportError:
    import config


class GameEngine:
    def __init__(
        self,
        grid_size=config.GRID_SIZE,
        ship_sizes=config.SHIP_SIZES,
        max_shots=config.MAX_SHOTS,
        ai_hit_chance=0.35,
    ):
        self.grid_size = grid_size
        self.ship_sizes = ship_sizes
        self.max_shots = max_shots
        self.ai_hit_chance = ai_hit_chance

        self.board = self.create_board()
        self.ships = []
        self.hit_coords = set()
        self.last_sunk_coords = []
        self.place_ships()

        self.player_board = self.create_board()
        self.player_ships = []

        self.shots_left = self.max_shots
        self.hits = 0
        self.total_ship_cells = sum(self.ship_sizes)

        # Temporary player health pool (matches total fleet HP until 2nd board is added)
        self.max_player_hp = self.total_ship_cells
        self.player_hp = self.max_player_hp

        self.game_over = False
        self.won = False
        self.loss_reason = None

    def create_board(self):
        return [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def get_ship_coords(self, start_r, start_c, size, orientation):
        if orientation == "hrztl":
            return [(start_r, start_c + i) for i in range(size)]
        return [(start_r + i, start_c) for i in range(size)]

    def can_place_ship(self, board, ship_coords):
        for r, c in ship_coords:
            if not (0 <= r < self.grid_size and 0 <= c < self.grid_size):
                return False
            if board[r][c] != 0:
                return False
        return True

    def place_player_ship(self, start_r, start_c, size, orientation):
        ship_coords = self.get_ship_coords(start_r, start_c, size, orientation)
        if not self.can_place_ship(self.player_board, ship_coords):
            return False

        for r, c in ship_coords:
            self.player_board[r][c] = 1
        self.player_ships.append(set(ship_coords))
        return True

    def place_ships(self):
        self.ships = []
        for size in self.ship_sizes:
            while True:
                orientation = random.choice(["hrztl", "vert"])
                start_r = random.randint(0, self.grid_size - 1)
                start_c = random.randint(0, self.grid_size - 1)
                ship_coords = self.get_ship_coords(start_r, start_c, size, orientation)

                if self.can_place_ship(self.board, ship_coords):
                    for r, c in ship_coords:
                        self.board[r][c] = 1
                    self.ships.append(set(ship_coords))
                    break

    def simulate_ai_turn(self):
        if random.random() < self.ai_hit_chance:
            self.player_hp = max(0, self.player_hp - 1)
            return True
        return False

    def fire_shot(self, r, c):
        if self.game_over:
            return "ignored"

        self.last_sunk_coords = []
        self.shots_left -= 1
        is_hit = self.board[r][c] == 1
        sunk_ship = False

        if is_hit:
            self.hits += 1
            self.hit_coords.add((r, c))
            for ship in self.ships:
                if (r, c) in ship and ship.issubset(self.hit_coords):
                    self.last_sunk_coords = list(ship)
                    sunk_ship = True
                    break

        if self.hits == self.total_ship_cells:
            self.game_over = True
            self.won = True
            return "sunk" if sunk_ship else "hit"

        # Enemy counter-attack (temporary HP simulation)
        self.simulate_ai_turn()

        if self.player_hp == 0:
            self.game_over = True
            self.won = False
            self.loss_reason = "hp"
        elif self.shots_left == 0:
            self.game_over = True
            self.won = False
            self.loss_reason = "ammo"

        if not is_hit:
            return "miss"
        return "sunk" if sunk_ship else "hit"
