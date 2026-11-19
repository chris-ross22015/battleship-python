# Battleship Python — Feature Backlog

## Phase 1: Core Architecture & CI (Completed)
- [x] Separate `GameEngine` logic from `tkinter` UI (`battleship/engine.py`)
- [x] Centralize gameplay configuration (`config.py`) and UI styling (`constants.py`)
- [x] Migrate to dedicated `battleship-python` repository with GitHub Actions CI (`ruff` + `pytest`)
- [x] Add automated unit tests for `GameEngine` (`tests/test_engine.py`)

## Phase 2: Full Two-Fleet Core Gameplay (Next Up)
- [ ] **Temp Player Health:** TEMPORARILY Track player health decreases by 1 randomly per PC turn max == max ship HP. Loss condition when 0
- [ ] **Per-Ship Sunk Detection:** Track individual ship coordinates so the engine and UI announce when a specific ship sinks
- [ ] **Player-Placed Ships (Place & Rotate):** Placement phase allowing the player to position and rotate their own fleet before battle starts
- [ ] **Second Board (Opponent Fleet & AI Turns):** Dual-board layout where the player fires at the enemy grid and an AI opponent fires back at the player's fleet


## Phase 3: Polish & Packaging
- [ ] **Resolution-Independent Responsive Layout:** Dynamically scale board tiles, HUD bars, and fonts to fit any desktop window, tablet, or phone aspect ratio without clipping or grid distortion
- [ ] **New Game / Reset Button:** Restart the match cleanly without closing the window
- [ ] **Difficulty Presets:** Small, Medium, and Large grid configurations (`grid_size`, `ship_sizes`, `max_shots`)
- [ ] **Terrain / Islands:** Impassable island tiles that block ship placement and soak up incoming shots (toggleable)
- [ ] ** AI Update
- [ ] **Executable / Standalone Packaging:** Bundle for desktop distribution

## Phase 4: Power-Ups, Themes & Assets
- [ ] **3x3 Radar Scan Ability:** Limited-use sonar ping that reveals the count of ship cells in a 3x3 area without dealing damage
- [ ] **Naval Mines:** Hidden hazard cells (`2`) that deduct extra ammo or trigger splash damage when struck
- [ ] **Theme Presets:** Classic Naval vs. Space Fleet styling via `constants.py`
- [ ] **Non-Traditional Ship Profiles:** Coordinate-offset ship templates (triangles, crosses, lollipops)
- [ ] **Custom Background Support:** Load custom board/backdrop images
- [ ] **Sound Effects & Visual Feedback:** Optional audio cues and animations on hit, miss, and sink
