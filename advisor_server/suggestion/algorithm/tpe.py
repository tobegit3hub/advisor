import json
import numpy as np
import hyperopt

from suggestion.models import Study
from suggestion.models import Trial
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.util import AlgorithmUtil


class TpeAlgorithm(AbstractSuggestionAlgorithm):

  def get_new_suggestions(self, study_id, trials=[], number=1):
    """
    Get the new suggested trials with random search.
    """

    search_space = hyperopt.hp.uniform('x', -10, 10)

    search_space_instance = search_space
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

    #import ipdb;ipdb.set_trace()


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


    """
    def _choose_tuner(self, algorithm_name):
      if algorithm_name == 'tpe':
        return hp.tpe.suggest
      if algorithm_name == 'random_search':
        return hp.rand.suggest
      if algorithm_name == 'anneal':
        return hp.anneal.suggest
      raise RuntimeError('Not support tuner algorithm in hyperopt.')
    """


    return_trial_list = []

    study = Study.objects.get(id=study_id)
    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    for i in range(number):
      trial = Trial.create(study.id, "TpeTrial")
      parameter_values_json = {}

      for param in params:

        if param["type"] == "INTEGER" or param["type"] == "DISCRETE" or param["type"] == "CATEGORICAL":
          pass

        elif param["type"] == "DOUBLE":
          # TODO: Get the specified value from hyperopt
          suggest_value = vals["x"][0]
          parameter_values_json[param["parameterName"]] = suggest_value

        parameter_values_json[param["parameterName"]] = suggest_value


      trial.parameter_values = json.dumps(parameter_values_json)
      trial.save()
      return_trial_list.append(trial)

    return return_trial_list
