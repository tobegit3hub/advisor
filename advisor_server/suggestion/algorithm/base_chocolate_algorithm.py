import json
import chocolate as choco

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm


class BaseChocolateAlgorithm(AbstractSuggestionAlgorithm):
  def __init__(self, algorithm_name="QuasiRandom"):

    self.algorithm_name = algorithm_name

  def get_new_suggestions(self, study_name, input_trials=[], number=1):
    """
    Get the new suggested trials with Chocolate algorithm.
    """

    # 1. Construct search space
    # Example: {"x" : choco.uniform(-6, 6), "y" : choco.uniform(-6, 6)}
    chocolate_search_space = {}

    study = Study.objects.get(name=study_name)
    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    for param in params:
      param_name = param["parameterName"]

      if param["type"] == "INTEGER":
        # TODO: Support int type of search space)
        pass

      elif param["type"] == "DOUBLE":
        chocolate_search_space[param_name] = choco.uniform(
            param["minValue"], param["maxValue"])

      elif param["type"] == "DISCRETE" or param["type"] == "CATEGORICAL":
        feasible_point_list = [
            value.strip() for value in param["feasiblePoints"].split(",")
        ]
        chocolate_search_space[param_name] = choco.choice(feasible_point_list)

    conn = choco.SQLiteConnection("sqlite:///my_db.db")

    # Refer to https://chocolate.readthedocs.io/tutorials/algo.html
    if self.algorithm_name == "Grid":
      sampler = choco.Grid(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "Random":
      sampler = choco.Random(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "QuasiRandom":
      sampler = choco.QuasiRandom(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "Bayes":
      sampler = choco.Bayes(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "CMAES":
      sampler = choco.CMAES(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "MOCMAES":
      mu = 1
      sampler = choco.MOCMAES(
          conn, chocolate_search_space, mu=mu, clear_db=True)

    # 2. Update with completed advisor trials
    completed_advisor_trials = Trial.objects.filter(
        study_name=study_name, status="Completed")

    for index, advisor_trial in enumerate(completed_advisor_trials):
      parameter_values_json = json.loads(advisor_trial.parameter_values)

      loss = advisor_trial.objective_value
      if study_configuration_json["goal"] == "MAXIMIZE":
        loss = -1 * loss

      entry = {"_chocolate_id": index, "_loss": loss}
      entry.update(parameter_values_json)
      # Should not use sampler.update(token, loss)
      conn.insert_result(entry)

    # 3. Run algorithm and construct return advisor trials
    return_trial_list = []

    for i in range(number):

      # Example: {'_chocolate_id': 1}
      # Example: {u'hidden2': u'32', u'learning_rate': 0.07122424534644338, u'l1_normalization': 0.8402644688674471, u'optimizer': u'adam'}
      token, chocolate_params = sampler.next()

      parameter_values_json = {}

      for param in params:

        if param["type"] == "INTEGER" or param["type"] == "DOUBLE" or param["type"] == "CATEGORICAL":
          parameter_values_json[param["parameterName"]] = chocolate_params[
              param["parameterName"]]
        elif param["type"] == "DISCRETE":
          parameter_values_json[param["parameterName"]] = int(
              chocolate_params[param["parameterName"]])

      new_advisor_trial = Trial.create(study.name, "ChocolateTrial")
      new_advisor_trial.parameter_values = json.dumps(parameter_values_json)
      new_advisor_trial.save()
      return_trial_list.append(new_advisor_trial)

    return return_trial_list
