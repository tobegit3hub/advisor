#!/usr/bin/env python

import argparse
from sklearn.datasets import make_classification
from sklearn.cross_validation import cross_val_score
from sklearn import svm

parser = argparse.ArgumentParser()
parser.add_argument("-gamma", type=float, default=0.001)
parser.add_argument("-C", type=float, default=0.5)
parser.add_argument("-kernel", type=str, default="sigmoid")
parser.add_argument("-coef0", type=float, default=0.1)
args = parser.parse_args()


def main():
  data, target = make_classification(
      n_samples=1000, n_features=45, n_informative=12, n_redundant=7)

  classifier = svm.SVC(
      gamma=args.gamma, C=args.C, kernel=args.kernel, coef0=args.coef0)

  score = cross_val_score(classifier, data, target, 'f1', cv=2).mean()
  print("Score: {}".format(score))
  return score


if __name__ == "__main__":
  main()
