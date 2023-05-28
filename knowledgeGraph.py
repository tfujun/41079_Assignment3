import networkx
import networkx as nx
import ast
import pandas
import matplotlib.pyplot as plt


class Archetype(object):
    def __init__(self, id, classname, winrate, popularity, name):
        self.id = id
        # also ignore name for now, since its in a separate file.
        # self.name = name
        self.classname = classname
        self.winrate = winrate
        self.popularity = popularity
        self.name = name
        # ignore core cards for now, don't know how to implement it

    def __str__(self):
        return self.name


class Variation(object):
    def __init__(self, archetype_id, id, winrate, popularity, k):
        self.archetype_id = archetype_id
        self.id = id
        self.winrate = winrate
        self.popularity = popularity

    def __str__(self):
        string = ""
        string += k.namedict[self.archetype_id]
        string += self.id
        return string


class Card(object):
    def __init__(self, row):
        # different constructors based on the type
        self.id = row[0]
        self.name = row[1]
        self.classname = row[2]
        self.cost = row[3]
        self.type = row[4]

    def __str__(self):
        return self.name


class KnowledgeGraph(object):
    def __init__(self):
        self.deckArchetype_path = "dataset/deck_archetype_March7-14.csv"
        self.archetypeName_path = "dataset/archetype_name_March7-14.csv"
        self.deckVariation_path = "dataset/deck_variation_March7-14.csv"
        self.cards_path = "dataset/card_stats.csv"
        self.coreCards_path = "dataset/core_cards_March7-14.json"
        self.deckCards_path = "dataset/deck_cards_March7-14.csv"
        self.archetypes = {}
        self.variations = {}
        self.cards = {}
        self.namedict = {}
        with open(self.archetypeName_path, "r") as names:
            names.readline()
            for row in names:
                data = row.split(",")
                self.namedict[data[0]] = data[1]
        self.G = nx.Graph()
        self.generate()

    def addArchetypes(self):
        print("-----Adding archetypes.")
        with open(self.deckArchetype_path, "r") as archetypes:
            archetypes.readline()
            for row in archetypes:
                data = row.split(",")
                a = Archetype(data[0], data[1], data[2], data[3], self.namedict[data[0]])
                self.archetypes[data[0]] = a
                self.G.add_node(a)
                # print(f"Added archetype with id {data[0]}")
        print("-----Completed adding archetypes.")

    def addVariants(self):
        print("-----Adding variations.")
        with open(self.deckVariation_path, "r") as variants:
            variants.readline()
            count = 0
            for row in variants:
                data = row.split(",")
                v = Variation(data[0], data[1], data[2], data[3], self)
                self.variations[data[1]] = v
                self.G.add_node(v)
                self.G.add_edge(self.archetypes[data[0]], v)
                # print(f"Added variation with id {data[1]} and archetype id {data[0]}")
                count += 1
                if count == 7000:
                    break
        print("-----Completed adding variations.")
        # del self.archetypes
        # technically don't need archetypes anymore.

    def addCards(self):
        print("-----Adding cards.")
        with open(self.cards_path, "r") as cards:
            print("Comprehending cards.")
            cards.readline()
            for row in cards:
                data = row.split(",")
                c = Card(data)
                self.cards[data[0]] = c
            print("Comprehension complete.")
        with open(self.deckCards_path, "r") as deckcards:
            print("Adding nodes and edges of cards.")
            deckcards.readline()
            for row in deckcards:
                data = row.split(",")
                cardlist = ast.literal_eval(row[row.find("\"")+1:-2])
                variationid = data[1]
                for card in cardlist:
                    self.G.add_edge(self.variations[variationid], self.cards[str(card[0])], weight=card[1])
            print("Adding nodes and edges to cards complete.")

    def generate(self):
        print("Generating graph...")
        self.addArchetypes()
        self.addVariants()
        self.addCards()

    def display_all(self):
        print("-----Attempting to display...")
        print("Creating colourmap.")
        colourmap = []
        for node in self.G:
            if type(node) == Archetype:
                colourmap.append("green")
            elif type(node) == Variation:
                colourmap.append("blue")
            elif type(node) == Card:
                colourmap.append("orange")
            else:
                colourmap.append("red")
        print("Drawing...")
        nx.draw(self.G, node_color=colourmap, with_labels=True, node_size=1200, font_size=8)
        print("Displaying.")
        plt.show()

    def display_archetype(self, archetype, limit=500):
        print(f"-----Attempting to display archetype {archetype}...")
        print("Creating colourmap.")
        nodes = [self.archetypes[str(archetype)]]
        variations = networkx.neighbors(self.G, self.archetypes[str(archetype)])
        count = 0
        for variation in variations:
            count += 1
            if count > limit:
                break
            nodes.append(variation)
            cards = networkx.neighbors(self.G, variation)
            for card in cards:
                nodes.append(card)
        subgraph = self.G.subgraph(nodes)
        colourmap = []
        for node in subgraph:
            if type(node) == Archetype:
                colourmap.append("green")
            elif type(node) == Variation:
                colourmap.append("blue")
            elif type(node) == Card:
                colourmap.append("orange")
            else:
                colourmap.append("red")
        print("Drawing...")
        pos = networkx.kamada_kawai_layout(subgraph)
        nx.draw(subgraph, node_color=colourmap, pos=pos, with_labels=True, font_size=8, node_size=1200)
        print("Displaying.")
        plt.show()


if __name__ == '__main__':
    k = KnowledgeGraph()
    # k.display_archetype(571, limit=10)
    print("pandas dataframe:")
    df = networkx.to_pandas_edgelist(k.G)
    # pandas.display(df)
    with open("output.txt", "w") as foo:
        for line in df.to_string():
            foo.write(line)
