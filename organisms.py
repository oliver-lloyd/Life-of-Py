import numpy as np


class Animal:
    """
    Blueprint for animals.
    """
    def __init__(self, species, diet, position, size, alive=True, parents=None, sex_ratio=0.5):
        self.species = species
        self.position = position
        self.size = size  # Could make this between 0-1, 1 for biggest animal
        self.diet = diet  # 'h'erbivore, 'c'arnivore, or 'o'mnivore
        self.alive = alive
        if np.random.uniform(0, 1) >= sex_ratio:
            self.sex = 'f'
        else:
            self.sex = 'm'
        if parents is None:
            self.quality = np.random.normal(0.5, 0.95/6, 1)
        elif len(parents) == 2:
            parents_quality = (parents[0].quality + parents[1].quality)/2
            self.quality = np.random.normal(parents_quality, 0.95/6, 1)

        self.age = 0
        self.energy = 0.5
        self.stress = 0
        self.mated_recently = False
        self.food_type = 'meat'
        self.pregnant = False

    def mate(self, target):
        if self.alive and target.alive and self.species == target.species:
            if self.sex != target.sex:
                quality_diff = np.abs(self.quality - target.quality)
                mate_chance = np.random.normal(1-quality_diff, 0.95/6, 1)
                if np.random.uniform(0, 1, 1) <= mate_chance:
                    self.socialise(target, intercourse=True)
                    if self.sex == 'f':
                        self.pregnant = True
                    else:
                        target.pregnant = True
            else:
                self.socialise(target, intercourse=True)

    def eat(self, target):
        # Eats the target food if it is a diet match and
        if self.diet == 'o':
            self.energy += target.size * (1-target.rot)
            del target
        elif self.diet == 'c' and target.food_type == 'meat':
            self.energy += target.size * (1 - target.rot)
            del target
        elif self.diet == 'h' and target.food_type == 'plant':
            self.energy += target.size * (1 - target.rot)
            del target

    def socialise(self, target, intercourse=False):
        # After a stress-proportional threshold is met, the stress levels of two intraspecific animals is reduced
        threshold = self.stress + target.stress
        if self.species == target.species and np.random.uniform(0, 2, 1) >= threshold:
            if intercourse:
                stress_heal = 0.5
            else:
                stress_heal = 0.2
            self.stress = max(self.stress - stress_heal, 0)
            target.stress = max(target.stress - stress_heal, 0)

    def move(self, target_loc, map_size, terrain_modifier):
        # Moves animal to target location, costing a certain amount of food in the process
        # Note: rework this to have species and quality modifiers to speed/food cost
        distance = np.linalg.norm(target_loc-self.position)
        self.energy -= (distance/map_size)*terrain_modifier

    def die(self):
        # Kills an animal
        self.alive = False

    def rot(self, rot_rate):
        # Decrease food value of animal after death
        if not self.alive:
            self.rot += rot_rate
