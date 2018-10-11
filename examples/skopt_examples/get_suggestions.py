#!/usr/bin/env python

from skopt import Optimizer


def f(parameters):
  # Example: [0.9578636327191035]

  x = parameters[0]
  y = x * x
  print("x: {}, y: {}".format(x, y))
  return y


opt = Optimizer([(-2.0, 2.0)])

for i in range(20):
  suggested = opt.ask()
  y = f(suggested)
  opt.tell(suggested, y)
  print('iteration:', i, suggested, y)
