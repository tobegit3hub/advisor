#!/usr/bin/env python

import hyperopt


def test_function(input):
  x = input["x"]
  y = x * 2 - 3 * x + 10
  # return {"loss": y, "status": hyperopt.STATUS_OK}
  return y


def main():

  # search_space = hyperopt.hp.uniform('x', -10, 10)
  search_space = {
      "x": hyperopt.hp.uniform('x', -10, 10),
      "x2": hyperopt.hp.uniform('x2', -10, 10)
  }

  trials = hyperopt.Trials()
  best = hyperopt.fmin(
      fn=test_function,
      space=search_space,
      algo=hyperopt.tpe.suggest,
      max_evals=100,
      trials=trials)
  print best


if __name__ == "__main__":
  main()
