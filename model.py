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

        # print(embeddingsDf.head())
        # To get a card from the df: embeddingsDf.loc[[self.knowledgeGraph.cards[{card_id}]]]
        # To reference a card object: self.knowledgeGraph.cards[{card_id}]
        # print(embeddingsDf.loc[[self.knowledgeGraph.cards["69640"]]])
        return embeddingsDf

class ModelTrainer(object):
    def __init__(self):
        self.preparedDataset = PrepareDataset()
        self.sourceCard = self.preparedDataset.knowledgeGraph.cards["78142"]
        self.predictedLinks = self.PredictLinks(self.preparedDataset.knowledgeGraph.G, self.preparedDataset.embeddingsDf, self.sourceCard)

    def PredictLinks(self, Graph, embeddingDf, sourceCard):
        card = embeddingDf[embeddingDf.index == sourceCard]
        print(card)

        allCards = Graph.nodes()
        otherNodes = [n for n in allCards if n not in list(Graph.adj[sourceCard]) + [sourceCard]]
        otherCards = embeddingDf[embeddingDf.index.isin(otherNodes)]

        similarity = cosine_similarity(card, otherCards)[0].tolist()
        index = otherCards.index.tolist()

        index_similarity = dict(zip(index, similarity))
        index_similarity = sorted(index_similarity.items(), key = lambda x: x[1], reverse = True)

        similarCards = index_similarity[:29]
        cards = [card[0] for card in similarCards]

        return cards

if __name__ == '__main__':
    model = ModelTrainer()
    print("Predicted links:")
    for predictedLink in model.predictedLinks:
        print(predictedLink)
