'''
Interact with genomes through species.
'''
import config
import random
# import gene
import gene1 as gene

# from genome import Genome
from genome1 import Genome


class NEAT:
	def __init__(self, inputs, outputs):
		god = Genome(inputs, outputs)
		self.Species = {0: [god]}

		for _ in range(config.POPULATION):
			clone = god.clone()
			clone.mutate()
			self.Species[0].append(clone)

		for _ in range(config.GENERATIONS):
			self.simulate()
			self.speciate()
			self.replicate()

		self.simulate()
		genomes = sum(self.Species.values(), [])
		genomes.sort(key=lambda genome: genome.fitness)
		top = genomes[-1]
		# for genome in genomes:
		# 	genome.print_genes()
		top.print_genes()
		# top.print_nodes()
		# top.predict()

	def simulate(self):
		for genome in sum(self.Species.values(), []):
			genome.fitness = len(genome.Genes)

	def speciate(self):
		''' Assign each genome to a species it is compatable with. '''
		next_species = {}
		randomized = sorted(sum(self.Species.values(), []), key=lambda L: random.random())
		for genome in randomized:
			for i, species in next_species.items():
				if species[0].compatable(genome):
					next_species[i].append(genome)
					break
			else:
				next_species[len(next_species)] = [genome]

		self.Species = {i: species for (i, species) in next_species.items() 
						if len(species) > config.species_size_threshold}

	def replicate(self):
		gene.Gene.reset()
		species_fitness = []
		for species in self.Species.values():
			species_fitness.append(sum([genome.fitness for genome in species]) / len(species))
		total_fitness = sum(species_fitness)

		for i, species in self.Species.items():
			species.sort(key=lambda genome: genome.fitness, reverse=True)
			allowed_offspring = int(species_fitness[i] / total_fitness * config.POPULATION / 2)
			
			offspring = [species[0]]
			for j in range(allowed_offspring):
				for _ in range(2):
					if j >= len(species):
						parent1 = random.choice(species)
					else:
						parent1 = species[j]

					if random.uniform(0, 1) < config.chance_mutate_no_crossover:
						kid = parent1.clone()
					else:
						if random.uniform(0, 1) < config.chance_interspecies_mate:
							parent2 = random.choice(sum(self.Species.values(), []))
						else:
							parent2 = random.choice(species)
						kid = parent1.crossover(parent2)

					kid.mutate()
					offspring.append(kid)

			self.Species[i] = offspring


NEAT(2, 1)

