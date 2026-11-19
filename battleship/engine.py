import random

try:
    from battleship import config
    from battleship.modules.ai import AIController
except ImportError:
    import config
    from modules.ai import AIController


class GameEngine:
    def __init__(self, grid_size=config.GRID_SIZE, ship_sizes=config.SHIP_SIZES, max_shots=config.MAX_SHOTS):
        # --- Match Configuration ---
        self.grid_size = grid_size
        self.ship_sizes = ship_sizes
        self.max_shots = max_shots
        self.total_ship_cells = sum(self.ship_sizes)

        # --- Enemy Board & AI Controller ---
        self.ai = AIController()
        self.board = self.create_board()
        self.ships = []
        self.hit_coords = set()
        self.last_sunk_coords = []
        self.ai_shots = {}
        self.ai_hit_coords = set()
        self.last_ai_shot = None
        self.last_ai_sunk_coords = []
        self.place_ships()

        # --- Player Fleet, Ammo & Health ---
        self.player_board = self.create_board()
        self.player_ships = []
        self.player_shots = {}
        self.shots_left = self.max_shots
        self.hits = 0
        self.max_player_hp = self.total_ship_cells
        self.player_hp = self.max_player_hp

        # --- Match Status ---
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
            if not (0 <= r < self.grid_size and 0 <= c < self.grid_size) or board[r][c] != 0:
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

    def _resolve_shot(self, board, ships, hit_coords, shots_dict, r, c):
        if board[r][c] != 1:
            shots_dict[(r, c)] = "miss"
            return "miss", []

        hit_coords.add((r, c))
        for ship in ships:
            if (r, c) in ship and ship.issubset(hit_coords):
                sunk_coords = list(ship)
                for coord in sunk_coords:
                    shots_dict[coord] = "sunk"
                return "sunk", sunk_coords

        shots_dict[(r, c)] = "hit"
        return "hit", []

    def _check_defeat(self):
        if self.player_hp == 0:
            self.game_over = True
            self.won = False
            self.loss_reason = "hp"
        elif self.shots_left == 0:
            self.game_over = True
            self.won = False
            self.loss_reason = "ammo"

    def execute_ai_turn(self):
        if self.game_over:
            return "ignored"

        target = self.ai.choose_target(self.grid_size, self.ai_shots)
        if target is None:
            return "ignored"

        r, c = target
        self.last_ai_shot = target
        result, self.last_ai_sunk_coords = self._resolve_shot(self.player_board, self.player_ships, self.ai_hit_coords, self.ai_shots, r, c)
        if result in ("hit", "sunk"):
            self.player_hp = max(0, self.player_hp - 1)

        self._check_defeat()
        return result

    def fire_shot(self, r, c):
        if self.game_over or (r, c) in self.player_shots:
            return "ignored"

        self.shots_left -= 1
        result, self.last_sunk_coords = self._resolve_shot(self.board, self.ships, self.hit_coords, self.player_shots, r, c)
        if result in ("hit", "sunk"):
            self.hits += 1

        if self.hits == self.total_ship_cells:
            self.game_over = True
            self.won = True
            return result

        self._check_defeat()
        return result