from dataclasses import dataclass


@dataclass
class Health:
    life: int = 100
    max_life: int = life

    def receive_damage(self, damage: int) -> None:
        new_life_points = self.life - abs(damage)
        self.life = new_life_points if new_life_points >= 0 else 0

    def recover(self, life_points: int):
        new_life_points = self.life + abs(life_points)
        self.life = new_life_points if new_life_points <= self.max_life else self.max_life

    def is_dead(self):
        return self.life <= 0

    def is_life_full(self):
        return self.life == self.max_life
