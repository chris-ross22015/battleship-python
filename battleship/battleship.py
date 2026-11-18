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
        self.buttons = self.build_grid()
        self.status_label = tk.Label(
            self.root,
            text=f"{constants.SHOTS_LABEL_PREFIX}: {self.engine.shots_left}",
            font=constants.STATUS_FONT,
        )
        self.status_label.grid(row=0, column=0, columnspan=config.GRID_SIZE, pady=5)

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
                    command=lambda r=r, c=c: self.on_square_click(r, c)
                )
                btn.grid(row=r + 1, column=c)
                row_buttons.append(btn)
            buttons.append(row_buttons)
        return buttons
    
    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                    btn.config(state="disabled")
    
    def on_square_click(self, r, c):
        result = self.engine.fire_shot(r, c)

        if result == "hit":
            self.buttons[r][c].config(
                text=constants.HIT_TEXT,
                font=constants.BTN_FONT,
                bg=constants.HIT_COLOR,
                state="disabled",
                fg=constants.HIT_TEXT_COLOR,
                disabledforeground=constants.HIT_TEXT_COLOR
            )
        
        
        elif result == "miss":
            self.buttons[r][c].config(
                text=constants.MISS_TEXT,
                font=constants.BTN_FONT,
                bg=constants.MISS_COLOR,
                state="disabled",
                fg=constants.MISS_TEXT_COLOR,
                disabledforeground=constants.MISS_TEXT_COLOR
            )

        self.status_label.config(text=f"{constants.SHOTS_LABEL_PREFIX}: {self.engine.shots_left}")

        if self.engine.game_over:
            if self.engine.won:
                self.status_label.config(text=constants.VICTORY_TEXT, fg=constants.VICTORY_COLOR)
            else:
                self.status_label.config(text=constants.GAME_OVER_AMMO, fg=constants.GAME_OVER_COLOR)
            self.disable_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
