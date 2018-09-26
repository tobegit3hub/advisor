#!/usr/bin/env python

import chocolate as choco


def himmelblau(x, y):
  return (x**2 + y - 11)**2 + (x + y**2 - 7)**2


def main():
  conn = choco.SQLiteConnection("sqlite:///my_db.db")
  # results = conn.results_as_dataframe()

  space = {"x": choco.uniform(-6, 6), "y": choco.uniform(-6, 6)}

  # Refer to https://chocolate.readthedocs.io/tutorials/algo.html
  sampler = choco.QuasiRandom(conn, space, clear_db=True)
  #sampler = choco.MOCMAES(conn, space, mu=0.1, clear_db=True)

  # Token: {'_chocolate_id': 0}
  # Params: {'y': 1.4641226269602674, 'x': 2.5223111999723393}
  token, params = sampler.next()
  loss = himmelblau(**params)
  sampler.update(token, loss)
  print("Token: {}, loss: {}".format(token, loss))

  """
  token = {'_chocolate_id': 2}
  chocolate_params = {'y': -4.666666666666667, 'x': 3.0}
  entry = {"_chocolate_id": 3, 'y': -4.666666666666667, 'x': 3.0, "_loss": 100}
  conn.insert_result(entry)
  """

if __name__ == "__main__":
  main()
