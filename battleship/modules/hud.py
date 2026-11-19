import tkinter as tk

try:
    from battleship import config, constants
except ImportError:
    import config
    import constants


class GameHUD:
    def __init__(self, root, on_rotate, on_toggle_view):
        self.status_label = tk.Label(
            root,
            text="",
            font=constants.STATUS_FONT,
            width=52,
        )
        self.status_label.grid(row=0, column=0, pady=(6, 4))

        self.rotate_btn = tk.Button(
            root,
            text="Rotate Ship (R): Horizontal",
            font=constants.ROTATE_BTN_FONT,
            command=on_rotate,
        )
        self.rotate_btn.grid(row=1, column=0, pady=(0, 6))

        self.battle_hud_frame = tk.Frame(root)

        self.hp_canvas = tk.Canvas(
            self.battle_hud_frame,
            width=constants.HP_BAR_WIDTH,
            height=constants.HP_BAR_HEIGHT,
            bg=constants.HP_BAR_BG,
            highlightthickness=1,
            highlightbackground=constants.HP_BAR_BORDER,
        )
        self.hp_fill = self.hp_canvas.create_rectangle(
            0,
            0,
            constants.HP_BAR_WIDTH,
            constants.HP_BAR_HEIGHT,
            fill=constants.HP_BAR_HIGH_COLOR,
            width=0,
        )
        self.hp_canvas.pack(side=tk.LEFT, padx=(0, 12))

        self.view_toggle_btn = tk.Button(
            self.battle_hud_frame,
            text=constants.FLEET_VIEW_BTN_TEXT,
            font=constants.VIEW_BTN_FONT,
            width=12,
            command=on_toggle_view,
        )
        self.view_toggle_btn.pack(side=tk.LEFT)

    def set_setup_status(self, ship_index, note=""):
        ship_size = config.SHIP_SIZES[ship_index]
        ship_num = ship_index + 1
        total_ships = len(config.SHIP_SIZES)
        base = f"Deploy Fleet ({ship_num}/{total_ships}) — Place Size-{ship_size} Ship"
        text = f"{base}  |  {note}" if note else base
        self.status_label.config(text=text)

    def set_battle_status(self, shots_left, player_hp, max_player_hp, event_note=""):
        base = (
            f"{constants.SHOTS_LABEL_PREFIX}: {shots_left}  |  "
            f"{constants.HP_LABEL_PREFIX}: {player_hp}/{max_player_hp}"
        )
        text = f"{base}  —  {event_note}" if event_note else base
        self.status_label.config(text=text)

    def set_game_over_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    def update_orientation_label(self, orientation):
        label = "Horizontal" if orientation == "hrztl" else "Vertical"
        self.rotate_btn.config(text=f"Rotate Ship (R): {label}")

    def switch_to_battle(self):
        self.rotate_btn.grid_remove()
        self.battle_hud_frame.grid(row=1, column=0, pady=(0, 6))
        self.view_toggle_btn.config(text=constants.FLEET_VIEW_BTN_TEXT)

    def set_view_toggle_label(self, viewing_player_fleet):
        btn_text = (
            constants.GAME_VIEW_BTN_TEXT
            if viewing_player_fleet
            else constants.FLEET_VIEW_BTN_TEXT
        )
        self.view_toggle_btn.config(text=btn_text)

    def update_health_bar(self, player_hp, max_player_hp):
        ratio = player_hp / max_player_hp if max_player_hp > 0 else 0
        fill_width = int(constants.HP_BAR_WIDTH * ratio)

        if ratio > 0.5:
            bar_color = constants.HP_BAR_HIGH_COLOR
        elif ratio > 0.25:
            bar_color = constants.HP_BAR_MID_COLOR
        else:
            bar_color = constants.HP_BAR_LOW_COLOR

        self.hp_canvas.coords(self.hp_fill, 0, 0, fill_width, constants.HP_BAR_HEIGHT)
        self.hp_canvas.itemconfig(self.hp_fill, fill=bar_color)
