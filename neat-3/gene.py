import random
import config
from copy import deepcopy


gene_c = config.Counter()
node_c = config.Counter(2)


class Gene:
    Genes = {}

    def __init__(self, in_node, out_node, weight=None):
        # self.links = {in_node: {out_node}}
        self.nodes = (in_node, out_node)
        self.weight = weight if weight else random.uniform(-1.0, 1.0)
        self.innovation = Gene.Genes.get(self.nodes, self.new_link())
        self.active = True


    ''' Dunders. '''
    def __str__(self):
        activation = 'ON' if self.active else 'OFF'
        return '|' + \
        f'{self.nodes[0]: >4}:{self.nodes[1]: <4}|' + \
        f'{self.weight: 9.4f}   |' + \
        f'{self.innovation: ^12}|' + \
        f'{activation: ^8}|'

    def __eq__(self, gene):
        return self.innovation == gene.innovation

    def __hash__(self):
        return self.innovation


    ''' Feed forward. '''
    def relu(self, X):
        return X * (X > 0)

    def tanh(self, X):
        return np.tanh(X)

    def sigmoid(self, X):
        return     1 / (1 + np.exp(-4.9 * X))


    ''' Simple functions. '''
    def mutate(self):
        if random.uniform(0, 1) < config.chance_mutate_weight_adjust:
            self.weight += random.uniform(0, 1)
        else:
            self.weight = random.uniform(0, 1)

    def randomize(self):
        self.active = random.uniform(0, 1) < config.chance_inherit_disabled_gene

    def clone(self):
        return deepcopy(self)

    def new_link(self):
        Gene.Genes[frozenset(self.nodes)] = gene_c.next
        return gene_c.count


    ''' Class methods. '''
    @classmethod
    def get_node(cls, node):
        ''' Find connections sharing same node. '''
        for (i, gene1) in enumerate(cls.Genes.keys()):
            for gene2 in list(cls.Genes.keys())[i+1:]:
                if gene1 ^ gene2 >= set(node) and gene1 & gene2:
                    print(node, gene1 & gene2)
                    return list(gene1 & gene2)[0]

        return node_c.next

    @classmethod
    def reset(cls):
        cls.Genes.clear()



