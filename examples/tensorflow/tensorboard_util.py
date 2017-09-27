#!/usr/bin/env python

import logging
import tensorflow as tf

from tensorflow.tensorboard.backend.event_processing.event_accumulator import EventAccumulator

logging.basicConfig(level=logging.DEBUG)

flags = tf.app.flags
flags.DEFINE_boolean("inspect", False, "Insepect the event file or not")
flags.DEFINE_string("logdir", "./output0", "Directory of event file")
flags.DEFINE_string("tag", "training/hptuning/metric",
                    "The tag of metric to get")
FLAGS = flags.FLAGS


def get_hyperparameters_metric(logdir, tag="training/hptuning/metric"):
  logging.debug("Load the event file: {}".format(logdir))

  tf_size_guidance = {
      'compressedHistograms': 10,
      'images': 0,
      'scalars': 100,
      'histograms': 1
  }

  event_acc = EventAccumulator(logdir, tf_size_guidance)
  event_acc.Reload()

  # print(event_acc.Tags())
  # Example: [ScalarEvent(wall_time=1505790770.455106, step=10000L, value=0.2937762141227722)]
  metrics = event_acc.Scalars(tag)
  return metrics


def main():
  metrics = get_hyperparameters_metric(FLAGS.logdir, FLAGS.tag)
  logging.info(metrics)


if __name__ == "__main__":
  main()
