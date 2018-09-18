import json
import numpy as np
import hyperopt

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm


class TpeAlgorithm(AbstractSuggestionAlgorithm):

  def get_new_suggestions(self, study_id, trials=[], number=1):
    """
    Get the new suggested trials with random search.
    """


    #search_space = hyperopt.hp.uniform('x', -10, 10)
    #search_space = {"l1_normalization": hyperopt.hp.uniform('l1_normalization', -10, 10), "learning_rate": hyperopt.hp.uniform('learning_rate', -10, 10)}
    #import ipdb;ipdb.set_trace()

    # Example: {"x": hyperopt.hp.uniform('x', -10, 10), "x2": hyperopt.hp.uniform('x2', -10, 10)}
    hyperopt_search_space = {}

    study = Study.objects.get(id=study_id)
    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    for param in params:
      param_name = param["parameterName"]

      if param["type"] == "INTEGER":
        # TODO: Support int type of search space)
        pass

      elif param["type"] == "DISCRETE" or param["type"] == "CATEGORICAL":
        feasible_point_list = [
          value.strip() for value in param["feasiblePoints"].split(",")
        ]
        hyperopt_search_space[param_name] = hyperopt.hp.choice(param_name, feasible_point_list)

      elif param["type"] == "DOUBLE":
        hyperopt_search_space[param_name] = hyperopt.hp.uniform(param_name, param["minValue"], param["maxValue"])


    search_space_instance = hyperopt_search_space
    rstate = np.random.RandomState()
    trials = hyperopt.Trials()
    domain = hyperopt.Domain(None, search_space_instance,
                       pass_expr_memo_ctrl=None)
    algorithm = hyperopt.tpe.suggest
    rval = hyperopt.FMinIter(algorithm, domain, trials, max_evals=-1, rstate=rstate, verbose=0)
    rval.catch_eval_exceptions = False

    algorithm = rval.algo
    new_ids = rval.trials.new_trial_ids(1)
    rval.trials.refresh()
    random_state = rval.rstate.randint(2**31-1)
    new_trials = algorithm(new_ids, rval.domain, trials, random_state)
    rval.trials.refresh()

    # Example: {'x': [8.721658602103911]}
    vals = new_trials[0]['misc']['vals']


    """
    parameter = dict()
    for key in vals:
      try:
        parameter[key] = vals[key][0].item()
      except Exception:
        parameter[key] = None
    """

    """
    trials =rval.trials

    trial = trials.new_trial_docs([new_id], rval_specs, rval_results, rval_miscs)[0]
    trial['result'] = {'loss': reward, 'status': 'ok'}
    trial['state'] = hp.JOB_STATE_DONE
    trials.insert_trial_docs([trial])
    trials.refresh()
    """

    # TODO: Support other algorithms from hyperopt
    """
    if algorithm_name == 'tpe':
      return hp.tpe.suggest
    if algorithm_name == 'random_search':
      return hp.rand.suggest
    if algorithm_name == 'anneal':
      return hp.anneal.suggest
    """


    return_trial_list = []

    study = Study.objects.get(id=study_id)
    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    for i in range(number):
      trial = Trial.create(study.id, "TpeTrial")
      parameter_values_json = {}

      for param in params:

        if param["type"] == "INTEGER":
          pass

        elif param["type"] == "DOUBLE":
          # TODO: Get the specified value from hyperopt
          #suggest_value = vals["x"][0]
          suggest_value = vals[param["parameterName"]][0]
          parameter_values_json[param["parameterName"]] = suggest_value

        elif param["type"] == "DISCRETE":
          feasible_point_list = [
            float(value.strip()) for value in param["feasiblePoints"].split(",")
          ]
          suggest_index = vals[param["parameterName"]][0]
          suggest_value = feasible_point_list[suggest_index]

        elif param["type"] == "CATEGORICAL":
          feasible_point_list = [
            value.strip() for value in param["feasiblePoints"].split(",")
          ]
          suggest_index = vals[param["parameterName"]][0]
          suggest_value = feasible_point_list[suggest_index]

        parameter_values_json[param["parameterName"]] = suggest_value


      trial.parameter_values = json.dumps(parameter_values_json)
      trial.save()
      return_trial_list.append(trial)

    return return_trial_list
