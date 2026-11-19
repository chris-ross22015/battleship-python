try:
    from battleship import config
except ImportError:
    import config


class FleetSetupController:
    def __init__(self, engine, board_view, hud, on_setup_complete):
        self.engine = engine
        self.board_view = board_view
        self.hud = hud
        self.on_setup_complete = on_setup_complete

        self.active = True
        self.current_ship_index = 0
        self.orientation = "hrztl"
        self.hover_coords = None

        self.hud.set_setup_status(self.current_ship_index)

    def toggle_orientation(self):
        if not self.active:
            return
        self.orientation = "vert" if self.orientation == "hrztl" else "hrztl"
        self.hud.update_orientation_label(self.orientation)
        if self.hover_coords is not None:
            self.preview_ship(*self.hover_coords)

    def preview_ship(self, r, c):
        self.board_view.render_setup_board(self.engine.player_board)
        size = config.SHIP_SIZES[self.current_ship_index]
        coords = self.engine.get_ship_coords(r, c, size, self.orientation)
        is_valid = self.engine.can_place_ship(self.engine.player_board, coords)

        for sr, sc in coords:
            self.board_view.set_tile_preview(sr, sc, is_valid)

    def on_tile_enter(self, r, c):
        if not self.active:
            return
        self.hover_coords = (r, c)
        self.preview_ship(r, c)

    def on_tile_leave(self):
        if not self.active:
            return
        self.hover_coords = None
        self.board_view.render_setup_board(self.engine.player_board)

    def handle_click(self, r, c):
        size = config.SHIP_SIZES[self.current_ship_index]
        placed = self.engine.place_player_ship(r, c, size, self.orientation)
        if not placed:
            self.hud.set_setup_status(self.current_ship_index, "Invalid position!")
            return

        self.current_ship_index += 1
        if self.current_ship_index >= len(config.SHIP_SIZES):
            self.active = False
            self.hover_coords = None
            self.on_setup_complete()
        else:
            self.board_view.render_setup_board(self.engine.player_board)
            self.hud.set_setup_status(self.current_ship_index)
