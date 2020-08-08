import sklearn
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer

class LDASummarizer():
    def __init__(self, corpus, num_topics=10):
        self.vectorizer = CountVectorizer(stop_words='english')
        self.lda = LDA(n_components=num_topics, random_state=0)
        self.corpus = corpus
        
        self.count_vectorized_corpus  = self.vectorizer.fit_transform(corpus)

        self.lda.fit(self.count_vectorized_corpus)
    
    def get_topic_breakdown(self, n_top_words=5):
        topic_words = {}
        vocab = self.vectorizer.get_feature_names()
        for topic_idx, comp in enumerate(self.lda.components_):
            word_idxs = np.argsort(comp)[::-1][:n_top_words]
            topic_words[f'Topic {topic_idx}'] = [vocab[i] for i in word_idxs]
        return topic_words
    
    def get_topics_in_documents(self, docs):
        topics_words = self.get_topic_breakdown()
        doc_topics = []
        for idx, topics in enumerate(self.lda.transform(docs)):
            order = np.argsort(topics)[::-1]
            doc_topics.append(topic_words[order[0]])
        return doc_topics
    
    def get_summary(self, num_top_docs=1):
        # top documents per topic:
        W = self.lda.transform(self.count_vectorized_corpus)
        doc_idx_list = []
        for topic_idx in range(len(self.lda.components_)):
            doc_idxs = np.argsort(W[:, topic_idx])[::-1][:num_top_docs]
            doc_idx_list.extend(doc_idxs)
        
        summary = []
        for idx in sorted(set(doc_idx_list)):
            summary.append(self.corpus[idx])

        return "\n\n".join(summary)
