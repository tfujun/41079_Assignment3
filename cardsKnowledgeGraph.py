import random
import networkx
import networkx as nx
import ast
import pandas
import matplotlib.pyplot as plt


class Card(object):
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.classname = row[2]
        self.cost = row[3]
        self.type = row[4]

    def __str__(self):
        return self.name


class KnowledgeGraph(object):
    def __init__(self):
        self.cards_path = "dataset/card_stats.csv"
        self.deckCards_path = "dataset/deck_cards_March7-14.csv"
        self.cards = {}
        self.G = nx.Graph()
        self.addNodes()

    def addNodes(self):
        print("-----Adding cards.")
        with open(self.cards_path, "r") as cards:
            print("Comprehending cards.")
            cards.readline()
            for row in cards:
                data = row.split(",")
                if data[1][0] == '"':
                    data[1] += data[2]
                    data.pop(2)
                c = Card(data)
                self.G.add_node(c)
                self.cards[data[0]] = c
            print("Comprehension complete.")
        with open(self.deckCards_path, "r") as deckcards:
            print("Adding nodes and edges of cards.")
            deckcards.readline()
            for row in deckcards:
                cardlist = ast.literal_eval(row[row.find("\"")+1:-2])
                for card1 in cardlist:
                    for card2 in cardlist:
                        if card1 == card2:
                            continue
                        if self.G.has_edge(self.cards[str(card1[0])], self.cards[str(card2[0])]):
                            self.G[self.cards[str(card1[0])]][self.cards[str(card2[0])]]["weight"] += 1
                        else:
                            self.G.add_edge(self.cards[str(card1[0])], self.cards[str(card2[0])], weight=1)
            print("Adding nodes and edges to cards complete.")

    def display(self):
        print("Drawing...")
        pos = networkx.kamada_kawai_layout(self.G)
        nx.draw(self.G, pos=pos, with_labels=True, font_size=8, node_size=1200)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        print("Displaying.")
        plt.show()

    def displayPartial(self, cardid):
        print(f"Card chosen: {self.cards[cardid].name}, id: {cardid}")
        nodes = [self.cards[cardid]]
        neighbours = nx.neighbors(self.G, nodes[0])
        for neighbour in neighbours:
            nodes.append(neighbour)
        subgraph = self.G.subgraph(nodes)
        colourmap = ['red' if node.id == cardid else 'yellow' for node in subgraph]
        print("Drawing...")
        pos = networkx.kamada_kawai_layout(subgraph)
        nx.draw(subgraph, node_color=colourmap, pos=pos, with_labels=True, font_size=8, node_size=1200, width=0.2)
        labels = nx.get_edge_attributes(subgraph, 'weight')
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels)
        print("Displaying.")
        plt.show()

    def displayPartialRandom(self, amount):
        for i in range(amount):
            cardid = random.choice(list(self.cards.keys()))
            self.displayPartial(cardid)

    def getDataFrame(self):
        return networkx.to_pandas_edgelist(self.G)


if __name__ == '__main__':
    k = KnowledgeGraph()
    # k.displayPartialRandom(5)
    print(k.getDataFrame())
