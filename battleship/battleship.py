import tkinter as tk

try:
    from battleship import config, constants
    from battleship.engine import GameEngine
    from battleship.modules.board_view import BoardView
    from battleship.modules.hud import GameHUD
    from battleship.modules.setup_controller import FleetSetupController
except ImportError:
    import config
    import constants
    from engine import GameEngine
    from modules.board_view import BoardView
    from modules.hud import GameHUD
    from modules.setup_controller import FleetSetupController

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.engine = GameEngine()
        self.viewing_player_fleet = False
        self.engine = GameEngine()
        self.viewing_player_fleet = False
        self.ai_turn_in_progress = False
        self.hud = GameHUD(
            root=self.root,
            on_rotate=self.toggle_orientation,
            on_toggle_view=self.toggle_board_view,
        )
        self.board_view = BoardView(
            root=self.root,
            on_tile_enter=self.on_tile_enter,
            on_tile_leave=self.on_tile_leave,
            on_tile_click=self.on_square_click,
        )
        self.setup = FleetSetupController(
            engine=self.engine,
            board_view=self.board_view,
            hud=self.hud,
            on_setup_complete=self.start_battle,
        )
        self.root.bind("<r>", self.toggle_orientation)
        self.root.bind("<R>", self.toggle_orientation)

    def toggle_orientation(self, _event=None):
        self.setup.toggle_orientation()

    def on_tile_enter(self, r, c):
        self.setup.on_tile_enter(r, c)

    def on_tile_leave(self):
        self.setup.on_tile_leave()

    def start_battle(self):
        self.viewing_player_fleet = False
        self.hud.switch_to_battle()
        self.hud.set_battle_status(
            self.engine.shots_left,
            self.engine.player_hp,
            self.engine.max_player_hp,
            "Battle Stations! Fire at will!",
        )
        self.render_active_board()

    def toggle_board_view(self):
        if self.setup.active or self.ai_turn_in_progress:
            return

        self.viewing_player_fleet = not self.viewing_player_fleet
        self.hud.set_view_toggle_label(self.viewing_player_fleet)
        self.render_active_board()

        if not self.engine.game_over:
            note = constants.FLEET_VIEW_STATUS_NOTE if self.viewing_player_fleet else ""
            self.hud.set_battle_status(
                self.engine.shots_left,
                self.engine.player_hp,
                self.engine.max_player_hp,
                note,
            )

    def render_active_board(self):
        if self.viewing_player_fleet:
            self.board_view.render_fleet_board(
                self.engine.player_board,
                self.engine.ai_shots,
                self.engine.last_ai_shot,
            )
        else:
            self.board_view.render_enemy_board(
                self.engine.player_shots,
                self.engine.game_over,
            )

    def on_square_click(self, r, c):
        if self.setup.active:
            self.setup.handle_click(r, c)
            return

        if self.viewing_player_fleet or self.ai_turn_in_progress:
            return

        result = self.engine.fire_shot(r, c)
        if result == "ignored":
            return

        event_note = ""
        if result == "sunk":
            self.board_view.mark_ship_sunk(self.engine.last_sunk_coords)
            event_note = "Enemy Ship Sunk!"
        elif result == "hit":
            self.board_view.set_tile_hit(r, c)
        elif result == "miss":
            self.board_view.set_tile_miss(r, c)

        self.hud.set_battle_status(
            self.engine.shots_left,
            self.engine.player_hp,
            self.engine.max_player_hp,
            event_note,
        )

        if self.engine.game_over:
            self.handle_game_over()
            return

        self.begin_ai_turn(event_note)

    def begin_ai_turn(self, player_event_note):
        self.ai_turn_in_progress = True
        self.hud.view_toggle_btn.config(state=tk.DISABLED)
        status_note = (
            f"{player_event_note} — {constants.AI_FIRING_STATUS_NOTE}"
            if player_event_note
            else constants.AI_FIRING_STATUS_NOTE
        )
        self.hud.set_battle_status(
            self.engine.shots_left,
            self.engine.player_hp,
            self.engine.max_player_hp,
            status_note,
        )
        self.root.after(constants.AI_TURN_DELAY_MS, self.resolve_ai_turn)

    def resolve_ai_turn(self):
        ai_result = self.engine.execute_ai_turn()
        self.viewing_player_fleet = True
        self.hud.set_view_toggle_label(True)
        self.render_active_board()
        self.hud.update_health_bar(self.engine.player_hp, self.engine.max_player_hp)

        if ai_result == "sunk":
            ai_note = constants.AI_SUNK_STATUS_NOTE
        elif ai_result == "hit":
            ai_note = constants.AI_HIT_STATUS_NOTE
        else:
            ai_note = constants.AI_MISS_STATUS_NOTE

        self.hud.set_battle_status(
            self.engine.shots_left,
            self.engine.player_hp,
            self.engine.max_player_hp,
            ai_note,
        )

        if self.engine.game_over:
            self.ai_turn_in_progress = False
            self.hud.view_toggle_btn.config(state=tk.NORMAL)
            self.handle_game_over()
            return

        self.root.after(constants.AI_RETURN_DELAY_MS, self.finish_ai_turn)

    def finish_ai_turn(self):
        self.ai_turn_in_progress = False
        self.viewing_player_fleet = False
        self.hud.view_toggle_btn.config(state=tk.NORMAL)
        self.hud.set_view_toggle_label(False)
        self.render_active_board()
        self.hud.set_battle_status(
            self.engine.shots_left,
            self.engine.player_hp,
            self.engine.max_player_hp,
        )

    def handle_game_over(self):
        if self.engine.won:
            self.hud.set_game_over_status(
                constants.VICTORY_TEXT, constants.VICTORY_COLOR
            )
        elif self.engine.loss_reason == "hp":
            self.hud.set_game_over_status(
                constants.GAME_OVER_HP, constants.GAME_OVER_COLOR
            )
        else:
            self.hud.set_game_over_status(
                constants.GAME_OVER_AMMO, constants.GAME_OVER_COLOR
            )
        self.board_view.disable_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
