# Configuration File

## YAML Example

```yaml
name: "demo"
algorithm: "BayesianOptimization"
trialNumber: 10
path: "./advisor_client/examples/python_function/"
command: "./min_function.py"
search_space:
  goal: "MINIMIZE"
  randomInitTrials: 3
  params:
    - parameterName: "x"
      type: "DOUBLE"
      minValue: -10.0
      maxValue: 10.0
```

## JSON Example

```json
{
  "name": "demo",
  "algorithm": "BayesianOptimization",
  "trialNumber": 10,
  "concurrency": 1,
  "path": "./advisor_client/examples/python_function/",
  "command": "./min_function.py",
  "search_space": {
      "goal": "MINIMIZE",
      "randomInitTrials": 3,
      "params": [
          {
              "parameterName": "x",
              "type": "DOUBLE",
              "minValue": -10.0,
              "maxValue": 10.0,
              "scalingType": "LINEAR"
          }
      ]
  }
}
```

