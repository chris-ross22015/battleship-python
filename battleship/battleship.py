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
        )
        self.status_label.grid(row=0, column=0, columnspan=config.GRID_SIZE, pady=(6, 2))

        self.hp_canvas = tk.Canvas(
            self.root,
            width=constants.HP_BAR_WIDTH,
            height=constants.HP_BAR_HEIGHT,
            bg=constants.HP_BAR_BG,
            highlightthickness=1,
            highlightbackground=constants.HP_BAR_BORDER,
        )
        self.hp_canvas.grid(row=1, column=0, columnspan=config.GRID_SIZE, pady=(0, 6))
        self.hp_fill = self.hp_canvas.create_rectangle(
            0,
            0,
            constants.HP_BAR_WIDTH,
            constants.HP_BAR_HEIGHT,
            fill=constants.HP_BAR_HIGH_COLOR,
            width=0,
        )

        self.buttons = self.build_grid()

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
        buttons = []
        for r in range(config.GRID_SIZE):
            row_buttons = []
            for c in range(config.GRID_SIZE):
                btn = tk.Button(
                    self.root,
                    width=constants.BTN_WIDTH,
                    height=constants.BTN_HEIGHT,
                    text=constants.WATER_TEXT,
                    bg=constants.WATER_COLOR,
                    command=lambda r=r, c=c: self.on_square_click(r, c),
                )
                btn.grid(row=r + 2, column=c)
                row_buttons.append(btn)
            buttons.append(row_buttons)
        return buttons

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def on_square_click(self, r, c):
        result = self.engine.fire_shot(r, c)
        event_note = ""

        if result in ("hit", "sunk"):
            is_sunk = result == "sunk"
            self.buttons[r][c].config(
                text=constants.SUNK_TEXT if is_sunk else constants.HIT_TEXT,
                font=constants.BTN_FONT,
                bg=constants.SUNK_COLOR if is_sunk else constants.HIT_COLOR,
                state="disabled",
                fg=constants.HIT_TEXT_COLOR,
                disabledforeground=constants.HIT_TEXT_COLOR,
            )
            if is_sunk:
                event_note = "Enemy Ship Sunk!"

        elif result == "miss":
            self.buttons[r][c].config(
                text=constants.MISS_TEXT,
                font=constants.BTN_FONT,
                bg=constants.MISS_COLOR,
                state="disabled",
                fg=constants.MISS_TEXT_COLOR,
                disabledforeground=constants.MISS_TEXT_COLOR,
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
