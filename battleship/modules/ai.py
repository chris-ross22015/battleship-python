import random


class AIController:
    def choose_target(self, grid_size, previous_shots):
        available_targets = [
            (r, c)
            for r in range(grid_size)
            for c in range(grid_size)
            if (r, c) not in previous_shots
        ]
        if not available_targets:
            return None
        return random.choice(available_targets)

