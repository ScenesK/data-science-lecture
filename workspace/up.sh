#!/bin/bash

pip freeze > requirements.txt
jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=$1 > notebook.log 2>&1 &
jupyter lab --allow-root --no-browser --ip=0.0.0.0 --port=$2 > lab.log 2>&1 &
jupyter nteract --allow-root --no-browser --ip=0.0.0.0 --port=$3 > nteract.log 2>&1
