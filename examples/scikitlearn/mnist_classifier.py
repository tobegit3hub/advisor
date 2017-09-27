#!/usr/bin/env python

from sklearn import datasets, svm, metrics

from scikitlearn_util import main


def train(**kwargs):
  # The example from http://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html#sphx-glr-auto-examples-classification-plot-digits-classification-py
  digits = datasets.load_digits()

  images_and_labels = list(zip(digits.images, digits.target))
  n_samples = len(digits.images)
  data = digits.images.reshape((n_samples, -1))

  classifier = svm.SVC(**kwargs)

  classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])

  expected = digits.target[n_samples // 2:]
  predicted = classifier.predict(data[n_samples // 2:])

  print("Classification report for classifier %s:\n%s\n" %
        (classifier, metrics.classification_report(expected, predicted)))

  accuracy = metrics.accuracy_score(expected, predicted)
  return accuracy


if __name__ == "__main__":
  main(train)
