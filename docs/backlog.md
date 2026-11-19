# Battleship Python — Feature Backlog

## Phase 1: Core Architecture & CI (Completed)
- [x] Separate `GameEngine` logic from `tkinter` UI (`battleship/engine.py`)
- [x] Centralize gameplay configuration (`config.py`) and UI styling (`constants.py`)
- [x] Migrate to dedicated `battleship-python` repository with GitHub Actions CI (`ruff` + `pytest`)
- [x] Add automated unit tests for `GameEngine` (`tests/test_engine.py`)

## Phase 2: Full Two-Fleet Core Gameplay (In Progress)
- [x] **Temp Player Health:** Temporarily track player health (decreases by 1 randomly per PC turn, max == total ship HP, loss condition at 0)
- [x] **Per-Ship Sunk Detection:** Track individual ship coordinates so the engine and UI stamp `SUNK` across every segment when a ship sinks
- [x] **10x10 Grid & Standardized Hex Palette:** Upgrade board dimensions to classic `10x10` and align all UI color constants to `#RRGGBB` hex codes
- [x] **Player-Placed Ships (Place & Rotate):** Setup phase allowing the player to preview, rotate (`R` / button), and position their own fleet before battle starts
- [X] **Fleet Viewscreen Toggle ("View My Fleet"):** Button during battle to switch the single `10x10` viewscreen between Enemy Waters and the player's placed fleet
- [ ] **Opponent Fleet & AI Turn Viewscreen:** Replace temporary random HP drain with real AI shots fired onto `player_board`, auto-switching to the player's fleet viewscreen during the AI's turn with visual shot feedback
- [ ] **Modularize UI (`battleship.py` Refactor):** Split `battleship.py` into focused helper modules (e.g., `board_view.py`, `hud.py`, `setup_controller.py`) for easier maintenance and clean 1-to-1 mapping to Unity C# components

## Phase 3: Polish & Packaging
- [ ] **Smart AI Hunt/Target Logic:** Upgrade AI from random shots to adjacent-cell hunting after scoring a hit
- [ ] **Terrain / Islands:** Impassable island tiles that block ship placement and soak up incoming shots (toggleable)
- [ ] **New Game / Reset Button:** Restart the match cleanly without closing the window
- [ ] **Difficulty Presets:** Small, Medium, and Large grid configurations (`grid_size`, `ship_sizes`, `max_shots`)
- [ ] **Resolution-Independent Responsive Layout:** Dynamically scale board tiles, HUD bars, and fonts to fit any desktop window, tablet, or phone aspect ratio without clipping or grid distortion
- [ ] **Executable / Standalone Packaging:** Bundle for desktop distribution

## Phase 4: Power-Ups, Themes & Assets
- [ ] **3x3 Radar Scan Ability:** Limited-use sonar ping that reveals the count of ship cells in a 3x3 area without dealing damage
- [ ] **Naval Mines:** Hidden hazard cells (`2`) that deduct extra ammo or trigger splash damage when struck
- [ ] **Theme Presets:** Classic Naval vs. Space Fleet styling via `constants.py`
- [ ] **Non-Traditional Ship Profiles:** Coordinate-offset ship templates (triangles, crosses, lollipops)
- [ ] **Custom Background Support:** Load custom board/backdrop images
- [ ] **Sound Effects & Visual Feedback:** Optional audio cues and animations on hit, miss, and sink
