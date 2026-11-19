import random


class AIController:
    def __init__(self, hit_chance=0.35):
        self.hit_chance = hit_chance

    def should_hit_player(self):
        return random.random() < self.hit_chance
