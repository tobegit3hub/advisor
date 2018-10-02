#!/usr/bin/env python

import argparse
from tqdm import tqdm
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

parser = argparse.ArgumentParser()
parser.add_argument("-min_child_weight", type=int, default=10)
parser.add_argument("-max_depth", type=int, default=10)
parser.add_argument("-gamma", type=float, default=5.0)
parser.add_argument("-alpha", type=float, default=5.0)
args = parser.parse_args()


def main():
  # Train data from https://www.kaggle.com/c/allstate-claims-severity
  train = pd.read_csv('./train.csv')
  categorical_columns = train.select_dtypes(include=['object']).columns

  for column in tqdm(categorical_columns):
    le = LabelEncoder()
    train[column] = le.fit_transform(train[column])

  y = train['loss']

  X = train.drop(['loss', 'id'], 1)
  xgtrain = xgb.DMatrix(X, label=y)

  num_rounds = 3
  random_state = 2016
  params = {
      'eta': 0.1,
      'silent': 1,
      'eval_metric': 'mae',
      'verbose_eval': True,
      'seed': random_state
  }
  params["min_child_weight"] = args.min_child_weight
  params["max_depth"] = args.max_depth
  params["gamma"] = args.gamma
  params["alpha"] = args.alpha

  cv_result = xgb.cv(
      params,
      xgtrain,
      num_boost_round=num_rounds,
      nfold=5,
      seed=random_state,
      callbacks=[xgb.callback.early_stop(10)])

  print(cv_result['test-mae-mean'].values[-1])


if __name__ == "__main__":
  main()
