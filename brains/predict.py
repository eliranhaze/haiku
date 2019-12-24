import cPickle as pkl
import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from data import get as get_data, DATA

class Prediction(object):

    PKL = '.prediction.pkl'
    PKL_SOURCES = '.sources.pkl'
    INSTANCE = None

    def __init__(self, source = DATA):
        training_size = 1000 # not really
        num_iter = 10**6 / training_size # scikit recommendation
        self.classifier = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier(
                loss='log', # logistic regression, which allows probability prediction
                penalty='l2',
                alpha=1e-3,
                n_iter=num_iter,
                random_state=42,
            )),
        ])
        self._train(source)

    @classmethod
    def get(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls.load()
        return cls.INSTANCE
       
    @classmethod
    def load(cls):
        if os.path.exists(cls.PKL) and os.path.exists(cls.PKL_SOURCES):
            last_sources = pkl.load(open(cls.PKL_SOURCES, 'rb'))
            if last_sources == DATA:
                prediction = pkl.load(open(cls.PKL, 'rb'))
                return prediction
        prediction = cls()
        pkl.dump(prediction, open(cls.PKL, 'wb'))
        pkl.dump(DATA, open(cls.PKL_SOURCES, 'wb'))
        return prediction

    def _train(self, source = DATA):
        data, target = self._get_data(source)
        self.classifier.fit(data, target)

    def _get_data(self, source):
        data, target = get_data(source)
        return data, target

    def predict(self, x):
        return self.classifier.predict_proba([x])[0]

