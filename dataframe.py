import networkx
import pandas
import knowledgeGraph
import matplotlib.pyplot as plt


class DataModel(object):
    def __init__(self):
        self.training_set = pandas.DataFrame
        self.testing_set = pandas.DataFrame
        self.kgraph = knowledgeGraph.KnowledgeGraph()
        self.createSets()

    def createSets(self):
        training = []
        testing = []
        for card in self.kgraph.cards.values():
            training.append(card)
            testing.append(card)
        classes = {'DEATHKNIGHT': 0, 'DEMONHUNTER': 0, 'DRUID': 0, 'HUNTER': 0, 'MAGE': 0, 'PALADIN': 0, 'PRIEST': 0,
                   'ROGUE': 0, 'SHAMAN': 0, 'WARLOCK': 0, 'WARRIOR': 0}
        for node in self.kgraph.archetypes.values():
            print(node.name[:-1])
            if classes[node.classname] < 2:
                training.append(node)
                variations = networkx.neighbors(self.kgraph.G, node)
                for variation in variations:
                    training.append(variation)
            else:
                testing.append(node)
                variations = networkx.neighbors(self.kgraph.G, node)
                for variation in variations:
                    testing.append(variation)
            classes[node.classname] += 1
        traininggraph = self.kgraph.G.subgraph(training)
        # colourmap = []
        # for node in traininggraph:
        #     if type(node) == knowledgeGraph.Archetype:
        #         colourmap.append("green")
        #     elif type(node) == knowledgeGraph.Variation:
        #         colourmap.append("blue")
        #     elif type(node) == knowledgeGraph.Card:
        #         colourmap.append("orange")
        #     else:
        #         colourmap.append("red")
        testinggraph = self.kgraph.G.subgraph(testing)
        # networkx.draw(traininggraph, node_color=colourmap, with_labels=True)
        # plt.show()
        # networkx.draw(testinggraph)
        # plt.show()
        self.training_set = networkx.to_pandas_edgelist(traininggraph)
        self.testing_set = networkx.to_pandas_edgelist(testinggraph)


if __name__ == '__main__':
    dm = DataModel()
    print(dm.training_set)
    print(dm.testing_set)
