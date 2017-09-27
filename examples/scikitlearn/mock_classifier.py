#!/usr/bin/env python

from sklearn.datasets import make_classification
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC

from scikitlearn_util import main


def train(**kwargs):
  data, target = make_classification(
      n_samples=1000, n_features=45, n_informative=12, n_redundant=7)

  score = cross_val_score(SVC(**kwargs), data, target, 'f1', cv=2).mean()
  print("Score: {}".format(score))
  return score


if __name__ == "__main__":
  main(train)
