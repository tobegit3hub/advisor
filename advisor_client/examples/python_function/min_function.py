#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x", type=float, default=0.0)
args = parser.parse_args()


def main():
  # Read parameters
  x = args.x

  # Compute or learning
  y = x * x - 2 * x + 1
  print("Formula: {}, input: {}, output: {}".format("y = x * x - 2 * x + 1", x,
                                                    y))

  # Output the metrics
  print(y)


if __name__ == "__main__":
  main()
