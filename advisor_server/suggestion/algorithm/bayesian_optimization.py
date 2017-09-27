# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json
import random
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from scipy.stats import norm
from scipy.optimize import minimize

from suggestion.models import Study
from suggestion.models import Trial
from base_algorithm import BaseSuggestionAlgorithm
from random_search import RandomSearchAlgorithm


class BayesianOptimizationDemo(object):
  def test_function2(self, x, y):
    return -x**2 - (y - 1)**2 + 1

  def test_function(self, x, y):
    # The best x is 2
    return np.exp(-(x - 2)**2) + np.exp(-(x - 6)**2 / 10) + 1 / (x**2 + 1)

  def test_bayes_optimizaion(self):
    print("Start bayesian optimization")

    # 1. Initialize parameters
    acquisition_fucntion_kappa = 5
    init_point_number = 3
    iteration_number = 3
    iteration_index = 0
    train_features = []
    train_labels = []

    gp = GaussianProcessRegressor(
        kernel=Matern(nu=2.5),
        n_restarts_optimizer=25, )

    bound_dict = {'x': (-4, 4), 'y': (-3, 3)}
    # Example: [[-4,  4], [-3,  3]]
    bounds = []
    for key in bound_dict.keys():
      bounds.append(bound_dict[key])
    # Example: ndarray([[-4,  4], [-3,  3]])
    bounds = np.asarray(bounds)

    # 2. Get init random samples
    # Example: array([-3.66909025, -1.93270006, 1.36095631])
    init_xs = np.random.uniform(-4, 4, size=init_point_number)
    # Example: array([-0.84486644, -0.95367483, 0.61358525])
    init_ys = np.random.uniform(-3, 3, size=init_point_number)

    # Example: [[-3.66909025, -0.84486644], [-1.93270006, -0.95367483], [1.36095631, 0.61358525]]
    init_points = []
    for i in range(init_point_number):
      init_points.append([init_xs[i], init_ys[i]])

    # Example: [-4.4555402320291684, -7.9016857176523114]
    init_labels = []
    for point in init_points:
      init_labels.append(self.test_function(point[0], point[1]))

    # 3. GP compute the prior
    train_features = np.asarray(init_points)
    train_labels = np.asarray(init_labels)
    current_max_label = train_labels.max()

    gp.fit(train_features, train_labels)

    # 4. Acquision function computes the max value
    # Example: [[-3.66909025, -0.84486644], [-1.93270006, -0.95367483], [1.36095631, 0.61358525], ...], shape is [100000, 2]
    x_tries = np.random.uniform(
        bounds[:, 0], bounds[:, 1], size=(100000, bounds.shape[0]))

    mean, std = gp.predict(x_tries, return_std=True)
    # Confidence bound criteria
    acquisition_fucntion_values = mean + acquisition_fucntion_kappa * std
    x_max = x_tries[acquisition_fucntion_values.argmax()]
    max_acquision_fucntion_value = acquisition_fucntion_values.max()

    x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
    print("Current max acquision function choose: {}".format(x_max))

    for i in range(iteration_number):
      iteration_index += 1

      # 5. Choose the best and compute to add in train dataset
      train_features = np.vstack((train_features, x_max.reshape((1, -1))))
      train_labels = np.append(train_labels,
                               self.test_function(x_max[0], x_max[1]))

      # 6. Re-compute gaussian process and acquistion function
      gp.fit(train_features, train_labels)

      # Update maximum value
      if train_labels[-1] > current_max_label:
        current_max_label = train_labels[-1]
        print("Get the better parameters!")

      x_tries = np.random.uniform(
          bounds[:, 0], bounds[:, 1], size=(100000, bounds.shape[0]))

      mean, std = gp.predict(x_tries, return_std=True)
      acquisition_fucntion_values = mean + acquisition_fucntion_kappa * std
      x_max = x_tries[acquisition_fucntion_values.argmax()]
      max_acquision_fucntion_value = acquisition_fucntion_values.max()

      x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
      print("Max label: {}, current label: {}, acquision function choose: {}".
            format(current_max_label, train_labels[-1], x_max))


class BayesianOptimization(BaseSuggestionAlgorithm):
  def get_random_value(self, min_value, max_value):
    return random.uniform(min_value, max_value)

  def get_new_suggestions(self, study_id, trials, number=1):
    # TODO: Only support retuning one trial

    study = Study.objects.get(id=study_id)
    completed_trials = Trial.objects.filter(
        study_id=study_id, status="Completed")

    study_configuration_json = json.loads(study.study_configuration)

    random_init_trials = study_configuration_json.get("randomInitTrials", 3)

    params = study_configuration_json["params"]

    # Use random search if it has less dataset
    if len(completed_trials) < random_init_trials:
      randomSearchAlgorithm = RandomSearchAlgorithm()
      return_trials = randomSearchAlgorithm.get_new_suggestions(
          study_id, trials)
      return return_trials

    else:
      return_trial = Trial.create(study.id, "BayesianOptimizationTrial")
      acquisition_fucntion_kappa = 5

      # Example: {'x': (-4, 4), 'y': (-3, 3)}
      bound_dict = {}

      for param in params:

        if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
          min_value = param["minValue"]
          max_value = param["maxValue"]
          bound_dict[param["parameterName"]] = (min_value, max_value)
        elif param["type"] == "DISCRETE":
          feasible_points_string = param["feasiblePoints"]
          feasible_points = [
              float(value.strip()) for value in feasible_points_string.split(",")
          ]
          feasible_points.sort()
          min_value = feasible_points[0]
          max_value = feasible_points[-1]
          bound_dict[param["parameterName"]] = (min_value, max_value)
        elif param["type"] == "CATEGORICAL":
          feasible_points_string = param["feasiblePoints"]
          feasible_points = [
              value.strip() for value in feasible_points_string.split(",")
          ]
          for feasible_point in feasible_points:
            parameter_name = "{}_{}".format(param["parameterName"],
                                            feasible_point)
            bound_dict[parameter_name] = (0, 1)

      bounds = []
      for key in bound_dict.keys():
        bounds.append(bound_dict[key])
      bounds = np.asarray(bounds)

      gp = GaussianProcessRegressor(
          kernel=Matern(nu=2.5),
          n_restarts_optimizer=25, )

      init_points = []
      init_labels = []
      """
      parametername_type_map = {}
      for param in params:
        parametername_type_map[param["parameterName"]] = param["type"]
      """

      for trial in completed_trials:
        # Example: {"learning_rate": 0.01, "optimizer": "ftrl"}
        parameter_values_json = json.loads(trial.parameter_values)
        # Example: [0.01]

        instance_features = []
        instance_label = trial.objective_value

        for param in params:

          if param["type"] == "DOUBLE" or param["type"] == "INTEGER" or param["type"] == "DISCRETE":
            instance_feature = parameter_values_json[param["parameterName"]]
            instance_features.append(instance_feature)
          elif param["type"] == "CATEGORICAL":
            feasible_points_string = param["feasiblePoints"]
            # Example: ["sgd", "adagrad", "adam", "ftrl"]
            feasible_points = [
                value.strip() for value in feasible_points_string.split(",")
            ]
            # Example: "ftrl"
            parameter_value = parameter_values_json[param["parameterName"]]
            for feasible_point in feasible_points:
              if feasible_point == parameter_value:
                instance_features.append(1)
              else:
                instance_features.append(0)

        init_points.append(instance_features)
        init_labels.append(instance_label)

      #import ipdb;ipdb.set_trace()

      train_features = np.asarray(init_points)
      train_labels = np.asarray(init_labels)
      current_max_label = train_labels.max()

      gp.fit(train_features, train_labels)

      # Example: [[-3.66909025, -0.84486644], [-1.93270006, -0.95367483], [1.36095631, 0.61358525], ...], shape is [100000, 2]
      x_tries = np.random.uniform(
          bounds[:, 0], bounds[:, 1], size=(100000, bounds.shape[0]))

      mean, std = gp.predict(x_tries, return_std=True)
      # Confidence bound criteria
      acquisition_fucntion_values = mean + acquisition_fucntion_kappa * std
      x_max = x_tries[acquisition_fucntion_values.argmax()]
      max_acquision_fucntion_value = acquisition_fucntion_values.max()

      # Example: [3993.864683994805, 44.15441513231316]
      x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
      print("Current max acquision function choose: {}".format(x_max))

      # Example: {"hidden2": 3993.864683994805, "hidden1": 44.15441513231316}
      suggested_parameter_values_json = {}

      index = 0
      """
      # Example: [0.1, 0.5, 0.3, 0.9]
      # Example: {"learning_rate": (0.01, 0.5), "hidden1": (40, 400), "optimizer_sgd": (0, 1), "optimizer_ftrl": (0, 1)}
      for key in bound_dict.keys():
        parameter_values_json[key] = x_max[index]
        index += 1
      """

      for param in params:

        if param["type"] == "DOUBLE" or param["type"] == "INTEGER" or param["type"] == "DISCRETE":
          suggested_parameter_values_json[param["parameterName"]] = x_max[
              index]
          index += 1

        elif param["type"] == "CATEGORICAL":
          feasible_points_string = param["feasiblePoints"]
          # Example: ["sgd", "adagrad", "adam", "ftrl"]
          feasible_points = [
              value.strip() for value in feasible_points_string.split(",")
          ]

          # 记录这4个值中数最大的，然后取到对应的字符串
          current_max = x_max[index]
          suggested_parameter_value = feasible_points[0]
          for feasible_point in feasible_points:
            if x_max[index] > current_max:
              current_max = x_max[index]
              suggested_parameter_value = feasible_point
            index += 1

          suggested_parameter_values_json[param[
              "parameterName"]] = suggested_parameter_value

      return_trial.parameter_values = json.dumps(
          suggested_parameter_values_json)
      return_trial.save()

    return [return_trial]
