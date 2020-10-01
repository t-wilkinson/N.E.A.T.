'''
Globals
'''
POPULATION = 150    # populaiton of each species
GENERATIONS = 20

# Mutation
chance_mutate_weight = 0.8
chance_mutate_weight_adjust = 0.9
chance_mutate_weight_randomize = 0.1

species_big_size = 100
species_size_to_keep = 0.5
species_size_threshold = 5
species_stagnations_allowed = 15

chance_inherit_disabled_gene = 0.75
chance_mutate_no_crossover = 0.25
chance_interspecies_mate = 0.001
chance_new_node = 0.03
chance_new_link_big_species = 0.3
chance_new_link = 0.05

# Compatability distance coefficients
C1 = 1.0
C2 = 1.0
C3 = 0.4
compatability_distance_threshold = 3.0


class Counter:
    def __init__(self, value=0, max=float('inf')):
        self._count = value
        self._max = max

    @property
    def count(self):
        return self._count - 1

    @property
    def max(self):
        if self._max == self.count + 1:
            return True
        return False

    @max.setter
    def max(self, value):
        self._max = value

    @property
    def next(self):
        if self._count >= self._max:
            self._count = 0
        self._count += 1
        return self._count - 1

    def __repr__(self):
        return repr(self._count)

    def reset(self):
        self._count = 0
