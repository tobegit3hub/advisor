# Linear Model

## Run in standalone

```
python -m trainer.task
```

Or run with hyperparameters.

```
python -m trainer.task --optimizer sgd --learning_rate 0.01 --max_epochs 100 --checkpoint_path ./checkpoint --model_path ./model --output_path ./tensorboard
```

## Run in distributed

Start the ps server.

```
CUDA_VISIBLE_DEVICES='' TF_CONFIG='{"cluster": {"ps": ["127.0.0.1:3001"], "worker": ["127.0.0.1:3002"], "master": ["127.0.0.1:3003"]}, "task": {"index": 0, "type": "ps"}}' python -m trainer.task
```

Start the worker.

```
CUDA_VISIBLE_DEVICES='0' TF_CONFIG='{"cluster": {"ps": ["127.0.0.1:3001"], "worker": ["127.0.0.1:3002"], "master": ["127.0.0.1:3003"]}, "task": {"index": 0, "type": "worker"}}' python -m trainer.task
```

Start the master.

```
CUDA_VISIBLE_DEVICES='1' TF_CONFIG='{"cluster": {"ps": ["127.0.0.1:3001"], "worker": ["127.0.0.1:3002"], "master": ["127.0.0.1:3003"]}, "task": {"index": 0, "type": "master"}}' python -m trainer.task
```

## Use cloud-ml

Package the application and upload to FDS.

```
python setup.py sdist --format=gztar
```
