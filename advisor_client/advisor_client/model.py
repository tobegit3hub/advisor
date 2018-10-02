class Study(object):
  def __init__(self,
               name,
               study_configuration,
               algorithm="BayesianOptimization",
               id=None,
               status=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.name = name.encode("utf-8")
    self.study_configuration = study_configuration
    self.algorithm = algorithm
    self.status = status
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "Id: {}, name: {}, study_configuration: {}, algorithm: {}".format(
        self.id, self.name, self.study_configuration, self.algorithm)

  def to_dict(self):
    return {
        "name": self.name,
        "study_configuration": self.study_configuration,
        "algorithm": self.algorithm
    }

  @classmethod
  def from_dict(self, dict):
    return Study(dict["name"], dict["study_configuration"], dict["algorithm"],
                 dict["id"], dict["status"], dict["created_time"],
                 dict["updated_time"])


class Trial(object):
  def __init__(self,
               study_name,
               name,
               parameter_values=None,
               objective_value=None,
               id=None,
               status=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.study_name = study_name.encode("utf-8")
    self.name = name
    self.parameter_values = parameter_values
    self.objective_value = objective_value
    self.status = status
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "Id: {}, study_name: {}, name: {}, parameter_values: {}, objective_value: {}".format(
        self.id, self.study_name, self.name, self.parameter_values,
        self.objective_value)

  def to_dict(self):
    return {"study_name": self.study_name, "name": self.name}

  @classmethod
  def from_dict(self, dict):
    return Trial(dict["study_name"], dict["name"], dict["parameter_values"],
                 dict["objective_value"], dict["id"], dict["status"],
                 dict["created_time"], dict["updated_time"])


class TrialMetric(object):
  def __init__(self,
               trial_id,
               training_step,
               objective_value,
               id=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.trial_id = trial_id
    self.training_step = training_step
    self.objective_value = objective_value
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "Id: {}, trial_id: {}, training_step: {}, objective_value: {}".format(
        self.id, self.trial_id, self.training_step, self.objective_value)

  def to_dict(self):
    return {
        "trial_id": self.trial_id,
        "training_step": self.training_step,
        "objective_value": self.objective_value
    }

  @classmethod
  def from_dict(self, dict):
    return TrialMetric(dict["trial_id"], dict["training_step"],
                       dict["objective_value"], dict["id"],
                       dict["created_time"], dict["updated_time"])
