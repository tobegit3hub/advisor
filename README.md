# Advisor

## Introduction

Advisor is the hyper parameters tuning system for black box optimization.

It is the open-source implementation of [Google Vizier](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46180.pdf) with these features.

* Get suggestions from API, WEB or CLI
* Support abstractions of Study and Trial
* Included search and early stop algorithms
* Recommend parameters with trained model
* Same programming interfaces as Google Vizier

## Algorithms

* [x] Random Search Algorithm
* [x] Grid Search Algorithm
* [x] Bayesian Optimization
* [ ] SMAC Algorithm
* [ ] CMA-ES Algorithm
* [x] Early Stop First Trial Algorithm
* [x] Early Stop Descending Algorithm
* [ ] Performance Curve Stop Algorithm

## Usage

### Advisor Server

Run the advisor server.

```
pip install -r ./requirements.txt

./manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000` in the browser.

### Docker Server

You can run the server with `docker` as well.

```
docker run -d -p 8000:8000 tobegit3hub/advisor
```

### Advisor Client

Install with `pip`.

```
pip install advisor_clients
```

Run with Python SDK.

```
client = AdvisorClient()

# Create the study
study_configuration = {
        "goal": "MAXIMIZE",
        "maxTrials": 5,
        "maxParallelTrials": 1,
        "params": [
                {
                        "parameterName": "hidden1",
                        "type": "INTEGER",
                        "minValue": 40,
                        "maxValue": 400,
                        "scalingType": "LINEAR"
                }
        ]
}
study = client.create_study("Study", study_configuration)

# Get suggested trials
trials = client.get_suggestions(study, 3)

# Complete the trial
client.complete_trial(trial, trial_metrics)
```

Run with command-line tool.

```
advisor study list

advisor trial list --study_id 1
```

Please checkout [examples](./examples) for more usage.

## Concepts

Study configuration describe the search space of parameters. It supports four types and here is the example.

```
{
  "goal": "MAXIMIZE",
  "randomInitTrials": 1,
  "maxTrials": 5,
  "maxParallelTrials": 1,
  "params": [
    {
      "parameterName": "hidden1",
      "type": "INTEGER",
      "minValue": 1,
      "maxValue": 10,
      "scalingType": "LINEAR"
    },
    {
      "parameterName": "learning_rate",
      "type": "DOUBLE",
      "minValue": 0.01,
      "maxValue": 0.5,
      "scalingType": "LINEAR"
    },
    {
      "parameterName": "hidden2",
      "type": "DISCRETE",
      "feasiblePoints": "8, 16, 32, 64",
      "scalingType": "LINEAR"
    },
    {
      "parameterName": "optimizer",
      "type": "CATEGORICAL",
      "feasiblePoints": "sgd, adagrad, adam, ftrl",
      "scalingType": "LINEAR"
    },
    {
      "parameterName": "batch_normalization",
      "type": "CATEGORICAL",
      "feasiblePoints": "true, false",
      "scalingType": "LINEAR"
    }
  ]
}
```

## Visualization

You can visualize one-dimentation Bayesian Optimization with the notebooks in [visualization](./visualization).

## Screenshots

List all the studies and create/delete the studies easily.

![study_list.png](./images/study_list.png)

List the detail of study and all the related trials.

![study_detail.png](./images/study_detail.png)

List all the trials and create/delete the trials easily.

![trial_list.png](./images/trial_list.png)

List the detail of trial and all the related metrics.

![trial_detail.png](./images/trial_detail.png)

