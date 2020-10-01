'''
Gene represents a neuron / gene.
Each gene specifies a link between two nodes.
Each node has a bias and each link has a weight.
'''
import config

from random import uniform
from copy import deepcopy


'''
Globals
'''
innovation_counter = config.Counter()
ID_counter = config.Counter()


'''
Classes
'''
class Node:
    ''' Node gene. '''
    def __init__(self,
            layer: str,
            ID: int=None,
        ):
        self.layer = layer
        self.bias = uniform(-2.0, 2.0)
        self.sending = []
        self.recieving = 0

        if ID is None or ID == ID_counter.count:
            self.ID = ID_counter.next
        else:
            self.ID = ID


    # ''' Feed forward. '''
    # def link(self, node, weight):
    #     # self.sending.append(node)
    #     # self.weight = weight
    #     node.recieving += 1

    # def prepare(self):
    #     node.max = node.recieving

    # def ready(self):
    #     if node.max == node.recieving:
    #         return True

    # def fire(self):
    #     node.recieving = node.max
    #     result = sigmoid(sum(self.results) + self.bias)
    #     # for node in self.sending:
    #     #     node.feed(result)
    #     # self.results.clear()

    # def feed(self, result):
    #     # self.results.append(result * self.weight)
    #     node.recieving += 1

    # def sigmoid(self, X):
    #     return 1 / (1 + np.exp(-4.9 * X))

    # def relu(self, X):
    #     return X * (X > 0)


    ''' Dunders. '''
    def __eq__(self, node):
        ''' Two nodes are equal if they have the same ID. '''
        return self is node

    def __hash__(self):
        return self.ID

    def __str__(self):
        return f'|{self.ID: ^ 5}|{self.layer: ^18}|{self.bias: 12.2f}       |'


class Link:
    ''' Gene class. '''
    def __init__(self,
        IN: int,
        OUT: int,
        weight: float,
    ):
        self.IN = IN
        self.OUT = OUT
        self.activation = True
        self.weight = weight if weight else uniform(-1.0, 1.0)


class Gene(Link):
    ''' Each gene is a Link class which is a link between two Nodes. '''
    Genes = []

    def __init__(self,
            IN: int,
            OUT: int,
            weight: float=None,
        ):
        super().__init__(IN, OUT, weight)
        # check if link has been created this generation
        # if so, make sure both links have the same innovation
        # if not, increment the global innovation number
        innovation = next((
            gene.innovation for gene in Gene.Genes
            if (gene.IN, gene.OUT) == (IN, OUT)
        ), None)
        if innovation:
            self.innovation = innovation
        else:
            Gene.Genes.append(self)
            self.innovation = innovation_counter.next


    # ''' Feed forward. '''
    # def feed(self):
    #     if self.IN.ready():
    #         self.IN.feed()

    ''' Dunders. '''
    def __str__(self):
        active = 'ON' if self.activation else 'OFF'
        return '|' + \
        f'{self.IN: >4}:{self.OUT: <4}|' + \
        f'{self.weight: 9.4f}   |' + \
        f'{self.innovation: ^12}|' + \
        f'{active: ^8}|'

    def __eq__(self, gene):
        return self.innovation == gene.innovation

    def __hash__(self):
        return self.innovation


    ''' Randomize. '''
    def mutate(self):
        if uniform(0, 1) < config.chance_mutate_weight_adjust:
            self.weight += uniform(0, 1)
        else:
            self.weight = uniform(0, 1)

    def randomize(self):
        self.activation = uniform(0, 1) < config.chance_inherit_disabled_gene

    def clone(self):
        return deepcopy(self)


    ''' Class methods. '''
    @classmethod
    def reset_generation(cls):
        cls.Genes.clear()

    @classmethod
    def get_node_id(cls, IN: int, OUT: int):
        ''' Find ID for IN -> OUT, if not found increase ID counter. '''
        for (i, gene1) in enumerate(cls.Genes):
            gene1 = frozenset((gene1.IN, gene1.OUT))

            for gene2 in cls.Genes[i+1:]:
                gene2 = frozenset((gene2.IN, gene2.OUT))

                if gene1 ^ gene2 == frozenset((IN, OUT)) and gene1 & gene2:
                    return list(gene1 & gene2)[0]

        return ID_counter.count


