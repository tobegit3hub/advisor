# SDK

## 创建客户端对象

```python
client = AdvisorClient()
```

## 创建Study

```python
study_configuration = {
  "goal":
  "MINIMIZE",
  "randomInitTrials":
  1,
  "maxTrials":
  5,
  "maxParallelTrials":
  1,
  "params": [
      {
          "parameterName": "gamma",
          "type": "DOUBLE",
          "minValue": 0.001,
          "maxValue": 0.01,
          "feasiblePoints": "",
          "scalingType": "LINEAR"
      },
      {
          "parameterName": "C",
          "type": "DOUBLE",
          "minValue": 0.5,
          "maxValue": 1.0,
          "feasiblePoints": "",
          "scalingType": "LINEAR"
      },
      {
          "parameterName": "kernel",
          "type": "CATEGORICAL",
          "minValue": 0,
          "maxValue": 0,
          "feasiblePoints": "linear, poly, rbf, sigmoid, precomputed",
          "scalingType": "LINEAR"
      },
      {
          "parameterName": "coef0",
          "type": "DOUBLE",
          "minValue": 0.0,
          "maxValue": 0.5,
          "feasiblePoints": "",
          "scalingType": "LINEAR"
      },
  ]
}
study = client.create_study("Study", study_configuration,
                          "BayesianOptimization")

```

## 获取Study

```python
study = client.get_study_by_id(6)
```

## 获取Trial

```python
trials = client.get_suggestions(study.id, 3)
```

## 生成参数

```python
parameter_value_dicts = []
for trial in trials:
  parameter_value_dict = json.loads(trial.parameter_values)
  print("The suggested parameters: {}".format(parameter_value_dict))
  parameter_value_dicts.append(parameter_value_dict)
```

## 运行训练

```python
metrics = []
for i in range(len(trials)):
  metric = train_function(**parameter_value_dicts[i])
  metrics.append(metric)
```
  
## 完成Trial

```python
for i in range(len(trials)):
  trial = trials[i]
  client.complete_trial_with_one_metric(trial, metrics[i])
is_done = client.is_study_done(study.id)
best_trial = client.get_best_trial(study.id)
print("The study: {}, best trial: {}".format(study, best_trial))
```