#!/usr/bin/env python

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_float("x", 1.0, "The float input")
FLAGS = flags.FLAGS


def main():
  # Read parameters
  x = FLAGS.x

  # Compute or learning
  y = x * x - 3 * x + 2
  print("Formula: {}, input: {}, output: {}".format("y = x * x - 3 * x + 2", x,
                                                    y))

  # Output the metrics
  print(y)


if __name__ == "__main__":
  main()
