import tkinter as tk

try:
    from battleship import config, constants
except ImportError:
    import config
    import constants


class BoardView:
    def __init__(self, root, on_tile_enter, on_tile_leave, on_tile_click):
        self.on_tile_click = on_tile_click
        self.grid_frame = tk.Frame(
            root,
            highlightthickness=constants.GRID_BORDER_WIDTH,
            highlightbackground=constants.SETUP_BORDER_COLOR,
        )
        self.grid_frame.grid(row=2, column=0, padx=10, pady=(0, 10))
        self.tiles = self._build_grid(on_tile_enter, on_tile_leave, on_tile_click)

    def _build_grid(self, on_tile_enter, on_tile_leave, on_tile_click):
        tiles = []
        center = constants.TILE_SIZE // 2
        for r in range(config.GRID_SIZE):
            row_tiles = []
            for c in range(config.GRID_SIZE):
                canvas = tk.Canvas(
                    self.grid_frame,
                    width=constants.TILE_SIZE,
                    height=constants.TILE_SIZE,
                    bg=constants.FLEET_WATER_COLOR,
                    bd=0,
                    highlightthickness=1,
                    highlightbackground=constants.TILE_BORDER_COLOR,
                )
                canvas.grid(row=r, column=c)
                text_id = canvas.create_text(
                    center,
                    center,
                    text=constants.WATER_TEXT,
                    font=constants.BTN_FONT,
                    fill=constants.TEXT_COLOR,
                )
                canvas.bind("<Enter>", lambda _e, r=r, c=c: on_tile_enter(r, c))
                canvas.bind("<Leave>", lambda _e: on_tile_leave())
                canvas.bind("<Button-1>", lambda _e, r=r, c=c: on_tile_click(r, c))
                row_tiles.append((canvas, text_id))
            tiles.append(row_tiles)
        return tiles

    def set_border_color(self, color):
        self.grid_frame.config(highlightbackground=color)

    def set_tile_water(self, r, c, water_color):
        canvas, text_id = self.tiles[r][c]
        canvas.config(bg=water_color)
        canvas.itemconfig(
            text_id,
            text=constants.WATER_TEXT,
            font=constants.BTN_FONT,
            fill=constants.TEXT_COLOR,
            angle=0,
        )

    def set_tile_ship(self, r, c):
        canvas, text_id = self.tiles[r][c]
        canvas.config(bg=constants.SHIP_COLOR)
        canvas.itemconfig(
            text_id,
            text=constants.SHIP_TEXT,
            font=constants.BTN_FONT,
            fill=constants.HIT_TEXT_COLOR,
            angle=0,
        )

    def set_tile_preview(self, r, c, is_valid):
        if 0 <= r < config.GRID_SIZE and 0 <= c < config.GRID_SIZE:
            canvas, _text_id = self.tiles[r][c]
            color = (
                constants.PREVIEW_VALID_COLOR
                if is_valid
                else constants.PREVIEW_INVALID_COLOR
            )
            canvas.config(bg=color)

    def set_tile_hit(self, r, c):
        canvas, text_id = self.tiles[r][c]
        canvas.unbind("<Button-1>")
        canvas.config(bg=constants.HIT_COLOR)
        canvas.itemconfig(
            text_id,
            text=constants.HIT_TEXT,
            font=constants.BTN_FONT,
            fill=constants.HIT_TEXT_COLOR,
            angle=0,
        )

    def set_tile_miss(self, r, c):
        canvas, text_id = self.tiles[r][c]
        canvas.unbind("<Button-1>")
        canvas.config(bg=constants.MISS_COLOR)
        canvas.itemconfig(
            text_id,
            text=constants.MISS_TEXT,
            font=constants.BTN_FONT,
            fill=constants.MISS_TEXT_COLOR,
            angle=0,
        )

    def mark_ship_sunk(self, coords):
        for r, c in coords:
            canvas, text_id = self.tiles[r][c]
            canvas.unbind("<Button-1>")
            canvas.config(bg=constants.SUNK_COLOR)
            canvas.itemconfig(
                text_id,
                text=constants.SUNK_TEXT,
                font=constants.SUNK_FONT,
                fill=constants.HIT_TEXT_COLOR,
                angle=constants.SUNK_ANGLE,
            )

    def disable_board(self):
        for row in self.tiles:
            for canvas, _text_id in row:
                canvas.unbind("<Button-1>")

    def render_setup_board(self, player_board):
        self.set_border_color(constants.SETUP_BORDER_COLOR)
        for r in range(config.GRID_SIZE):
            for c in range(config.GRID_SIZE):
                if player_board[r][c] == 1:
                    self.set_tile_ship(r, c)
                else:
                    self.set_tile_water(r, c, constants.FLEET_WATER_COLOR)

    def render_fleet_board(self, player_board, ai_shots):
        self.set_border_color(constants.FLEET_VIEW_BORDER_COLOR)
        for r in range(config.GRID_SIZE):
            for c in range(config.GRID_SIZE):
                canvas, _text_id = self.tiles[r][c]
                canvas.unbind("<Button-1>")
                shot_state = ai_shots.get((r, c))

                if shot_state == "sunk":
                    self.mark_ship_sunk([(r, c)])
                elif shot_state == "hit":
                    self.set_tile_hit(r, c)
                elif shot_state == "miss":
                    self.set_tile_miss(r, c)
                elif player_board[r][c] == 1:
                    self.set_tile_ship(r, c)
                else:
                    self.set_tile_water(r, c, constants.FLEET_WATER_COLOR)

    def render_enemy_board(self, player_shots, game_over):
        self.set_border_color(constants.GAME_VIEW_BORDER_COLOR)
        for r in range(config.GRID_SIZE):
            for c in range(config.GRID_SIZE):
                canvas, _text_id = self.tiles[r][c]
                shot_state = player_shots.get((r, c))

                if shot_state == "sunk":
                    self.mark_ship_sunk([(r, c)])
                elif shot_state == "hit":
                    self.set_tile_hit(r, c)
                elif shot_state == "miss":
                    self.set_tile_miss(r, c)
                else:
                    self.set_tile_water(r, c, constants.WATER_COLOR)
                    if game_over:
                        canvas.unbind("<Button-1>")
                    else:
                        canvas.bind(
                            "<Button-1>", lambda _e, r=r, c=c: self.on_tile_click(r, c)
                        )
