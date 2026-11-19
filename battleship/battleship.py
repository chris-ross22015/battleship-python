import tkinter as tk

try:
    from battleship import config, constants
    from battleship.engine import GameEngine
except ImportError:
    import config
    import constants
    from engine import GameEngine


class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.engine = GameEngine()

        self.status_label = tk.Label(
            self.root,
            text=self.format_status(),
            font=constants.STATUS_FONT,
            width=44,
        )
        self.status_label.grid(row=0, column=0, pady=(6, 2))

        self.hp_canvas = tk.Canvas(
            self.root,
            width=constants.HP_BAR_WIDTH,
            height=constants.HP_BAR_HEIGHT,
            bg=constants.HP_BAR_BG,
            highlightthickness=1,
            highlightbackground=constants.HP_BAR_BORDER,
        )
        self.hp_canvas.grid(row=1, column=0, pady=(0, 6))
        self.hp_fill = self.hp_canvas.create_rectangle(
            0,
            0,
            constants.HP_BAR_WIDTH,
            constants.HP_BAR_HEIGHT,
            fill=constants.HP_BAR_HIGH_COLOR,
            width=0,
        )

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=2, column=0, padx=8, pady=(0, 8))
        self.tiles = self.build_grid()

    def format_status(self, event_note=""):
        base = (
            f"{constants.SHOTS_LABEL_PREFIX}: {self.engine.shots_left}  |  "
            f"{constants.HP_LABEL_PREFIX}: {self.engine.player_hp}/{self.engine.max_player_hp}"
        )
        return f"{base}  —  {event_note}" if event_note else base

    def update_health_bar(self):
        ratio = (
            self.engine.player_hp / self.engine.max_player_hp
            if self.engine.max_player_hp > 0
            else 0
        )
        fill_width = int(constants.HP_BAR_WIDTH * ratio)

        if ratio > 0.5:
            bar_color = constants.HP_BAR_HIGH_COLOR
        elif ratio > 0.25:
            bar_color = constants.HP_BAR_MID_COLOR
        else:
            bar_color = constants.HP_BAR_LOW_COLOR

        self.hp_canvas.coords(self.hp_fill, 0, 0, fill_width, constants.HP_BAR_HEIGHT)
        self.hp_canvas.itemconfig(self.hp_fill, fill=bar_color)

    def build_grid(self):
        tiles = []
        center = constants.TILE_SIZE // 2
        for r in range(config.GRID_SIZE):
            row_tiles = []
            for c in range(config.GRID_SIZE):
                canvas = tk.Canvas(
                    self.grid_frame,
                    width=constants.TILE_SIZE,
                    height=constants.TILE_SIZE,
                    bg=constants.WATER_COLOR,
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
                canvas.bind("<Button-1>", lambda _event, r=r, c=c: self.on_square_click(r, c))
                row_tiles.append((canvas, text_id))
            tiles.append(row_tiles)
        return tiles


    def mark_ship_sunk(self, coords):
        for sr, sc in coords:
            tile_canvas, tile_text_id = self.tiles[sr][sc]
            tile_canvas.config(bg=constants.SUNK_COLOR)
            tile_canvas.itemconfig(
                tile_text_id,
                text=constants.SUNK_TEXT,
                font=constants.SUNK_FONT,
                fill=constants.HIT_TEXT_COLOR,
                angle=constants.SUNK_ANGLE,
            )

    def disable_board(self):
        for row in self.tiles:
            for canvas, _text_id in row:
                canvas.unbind("<Button-1>")

    def on_square_click(self, r, c):
        canvas, text_id = self.tiles[r][c]
        canvas.unbind("<Button-1>")

        result = self.engine.fire_shot(r, c)
        event_note = ""

        if result in ("hit", "sunk"):
            if result == "sunk":
                self.mark_ship_sunk(self.engine.last_sunk_coords)
                event_note = "Enemy Ship Sunk!"
            else:
                canvas.config(bg=constants.HIT_COLOR)
                canvas.itemconfig(
                    text_id,
                    text=constants.HIT_TEXT,
                    font=constants.BTN_FONT,
                    fill=constants.HIT_TEXT_COLOR,
                    angle=0,
                )


        elif result == "miss":
            canvas.config(bg=constants.MISS_COLOR)
            canvas.itemconfig(
                text_id,
                text=constants.MISS_TEXT,
                font=constants.BTN_FONT,
                fill=constants.MISS_TEXT_COLOR,
                angle=0,
            )

        self.update_health_bar()
        self.status_label.config(text=self.format_status(event_note))

        if self.engine.game_over:
            if self.engine.won:
                self.status_label.config(text=constants.VICTORY_TEXT, fg=constants.VICTORY_COLOR)
            elif self.engine.loss_reason == "hp":
                self.status_label.config(text=constants.GAME_OVER_HP, fg=constants.GAME_OVER_COLOR)
            else:
                self.status_label.config(text=constants.GAME_OVER_AMMO, fg=constants.GAME_OVER_COLOR)
            self.disable_board()


if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
