#!/bin/bash

./manage.py runserver 0.0.0.0:8000 --noreload
# nohup ./manage.py runserver 0.0.0.0:80 &

# ipython notebook --config ./jupyter_notebook_config.py
# nohup ipython notebook --config ./jupyter_notebook_config.py --allow-root &
