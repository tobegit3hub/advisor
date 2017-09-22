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
    trials = Trial.objects.filter(study_id=study_id, status="Completed")

    return_trial = Trial.create(study.id, "BayesianOptimizationTrial")

    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    # Use random search if it has less than 3 dataset
    if len(trials) < 3:
      parameter_values_json = {}

      for param in params:
        min_value = param["minValue"]
        max_value = param["maxValue"]
        random_value = self.get_random_value(min_value, max_value)
        parameter_values_json[param["parameterName"]] = random_value

        return_trial.parameter_values = json.dumps(parameter_values_json)
        return_trial.save()

    else:
      acquisition_fucntion_kappa = 5

      # Example: {'x': (-4, 4), 'y': (-3, 3)}
      bound_dict = {}

      for param in params:
        min_value = param["minValue"]
        max_value = param["maxValue"]
        bound_dict[param["parameterName"]] = (min_value, max_value)

      bounds = []
      for key in bound_dict.keys():
        bounds.append(bound_dict[key])
      bounds = np.asarray(bounds)

      gp = GaussianProcessRegressor(
          kernel=Matern(nu=2.5),
          n_restarts_optimizer=25, )

      init_points = []
      init_labels = []
      for trial in trials:
        # {"learning_rate": 0.01}
        parameter_values_json = json.loads(trial.parameter_values)
        trial_point = []
        for param in params:
          trial_point.append(parameter_values_json[param["parameterName"]])

        init_points.append(trial_point)
        init_labels.append(trial.objective_value)

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

      x_max = np.clip(x_max, bounds[:, 0], bounds[:, 1])
      print("Current max acquision function choose: {}".format(x_max))

      # TODO: Support to generate parameter values
      parameter_values_json = {"hidden1": x_max[0]}
      return_trial.parameter_values = json.dumps(parameter_values_json)
      return_trial.save()

    return [return_trial]
