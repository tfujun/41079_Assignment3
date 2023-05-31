import cardsKnowledgeGraph
from node2vec import Node2Vec
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class PrepareDataset(object):
    def __init__(self):
        self.knowledgeGraph = cardsKnowledgeGraph.KnowledgeGraph()
        self.embeddingsDf = self.trainNode2Vec()
    
    def trainNode2Vec(self):
        trainer = Node2Vec(self.knowledgeGraph.G, dimensions=16)
        
        model = trainer.fit()

        embeddingsDf = (
            pd.DataFrame(
                [model.wv.get_vector(str(n)) for n in self.knowledgeGraph.G.nodes()],
                index = self.knowledgeGraph.G.nodes
            )
        )

        print(embeddingsDf.head())
        # print(embeddingsDf.index.astype(dtype=object))
        print(embeddingsDf[self.knowledgeGraph.G.nodes(self.knowledgeGraph.cards["69640"].name)])
        # print(embeddingsDf["Brawl"])
        return embeddingsDf

class ModelTrainer(object):
    def __init__(self):
        self.PreparedDataset = PrepareDataset()
        self.predictedLinks = self.PredictLinks(self.PreparedDataset.knowledgeGraph.G, self.PreparedDataset.embeddingsDf, "Brawl")

    def PredictLinks(self, Graph, embeddingDf, cardName):
        card = embeddingDf[embeddingDf.index == cardName]
        print(card)

        allCards = Graph.nodes()
        otherNodes = [n for n in allCards if n not in list(Graph.adj[cardName]) + [cardName]]
        otherCards = embeddingDf[embeddingDf.index.isin(otherNodes)]

        similarity = cosine_similarity(card, otherCards)[0].tolist()
        index = otherCards.index.tolist()

        index_similarity = dict(zip(index, similarity))
        index_similarity = sorted(index_similarity.items(), key = lambda x: x[1], reverse = True)

        similarCards = index_similarity[:30]
        cards = [card[0] for card in similarCards]
        return cards

if __name__ == '__main__':
    model = ModelTrainer()
    # print(model.predictedLinks)
