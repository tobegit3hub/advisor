#!/usr/bin/env python

from advisor_client.model import Study
from advisor_client.model import Trial
from advisor_client.model import TrialMetric
from advisor_client.client import AdvisorClient

client = AdvisorClient()

# Create Study
name = "Study"
study_configuration = {
    "goal":
    "MAXIMIZE",
    "maxTrials":
    5,
    "maxParallelTrials":
    1,
    "params": [{
        "parameterName": "hidden1",
        "type": "INTEGER",
        "minValue": 40,
        "maxValue": 400,
        "scallingType": "LINEAR"
    }]
}

study = client.create_study(name, study_configuration)
print(study)
print(client.list_studies())

trials = client.get_suggestions(study.id, 3)
print(trials)
print(client.list_trials(study.id))
