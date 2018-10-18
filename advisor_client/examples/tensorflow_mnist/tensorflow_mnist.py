#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

flags = tf.app.flags
# TODO: Change to int if advisor support DISCRETE with int
flags.DEFINE_float("batch_size", 64.0, "")
flags.DEFINE_float("batch_number", 938.0, "")
flags.DEFINE_string("optimizer", "sgd", "")
flags.DEFINE_float("learning_rate", 0.01, "")
FLAGS = flags.FLAGS


def get_optimizer_by_name(optimizer_name, learning_rate):
  """
    Get optimizer object by the optimizer name.

    Args:
      optimizer_name: Name of the optimizer.
      learning_rate: The learning rate.

    Return:
      The optimizer object.
    """

  if optimizer_name == "sgd":
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  elif optimizer_name == "adadelta":
    optimizer = tf.train.AdadeltaOptimizer(learning_rate)
  elif optimizer_name == "adagrad":
    optimizer = tf.train.AdagradOptimizer(learning_rate)
  elif optimizer_name == "adam":
    optimizer = tf.train.AdamOptimizer(learning_rate)
  elif optimizer_name == "ftrl":
    optimizer = tf.train.FtrlOptimizer(learning_rate)
  elif optimizer_name == "rmsprop":
    optimizer = tf.train.RMSPropOptimizer(learning_rate)
  else:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  return optimizer


def main():
  mnist = input_data.read_data_sets("/tmp/tensorflow/mnist/input_data")

  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.matmul(x, W) + b

  y_ = tf.placeholder(tf.int64, [None])
  cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y)
  optimizer = get_optimizer_by_name(FLAGS.optimizer, FLAGS.learning_rate)
  train_step = optimizer.minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()

  for i in range(int(FLAGS.batch_number)):
    #batch_xs, batch_ys = mnist.train.next_batch(100)
    batch_xs, batch_ys = mnist.train.next_batch(int(FLAGS.batch_size))
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    if i % 100 == 0:
      print("Run batch")

  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), y_)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(
      accuracy, feed_dict={x: mnist.test.images,
                           y_: mnist.test.labels}))


if __name__ == "__main__":
  main()
