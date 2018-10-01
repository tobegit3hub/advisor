#!/usr/bin/env python

import argparse
from sklearn import datasets, svm, metrics

parser = argparse.ArgumentParser()
parser.add_argument("-gamma", type=float, default=0.001)
parser.add_argument("-C", type=float, default=0.5)
parser.add_argument("-kernel", type=str, default="sigmoid")
parser.add_argument("-coef0", type=float, default=0.1)
args = parser.parse_args()


def main():
  # The example from http://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html#sphx-glr-auto-examples-classification-plot-digits-classification-py
  digits = datasets.load_digits()

  images_and_labels = list(zip(digits.images, digits.target))
  n_samples = len(digits.images)
  data = digits.images.reshape((n_samples, -1))

  classifier = svm.SVC(
      gamma=args.gamma, C=args.C, kernel=args.kernel, coef0=args.coef0)

  classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])

  expected = digits.target[n_samples // 2:]
  predicted = classifier.predict(data[n_samples // 2:])

  print("Classification report for classifier %s:\n%s\n" %
        (classifier, metrics.classification_report(expected, predicted)))

  accuracy = metrics.accuracy_score(expected, predicted)

  print(accuracy)


if __name__ == "__main__":
  main()
