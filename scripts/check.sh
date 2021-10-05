#!/bin/bash 
# to run before pushing

echo running pylint 
python -m pylint -E `dirname */__init__.py` bin
echo running pytest 
python -m pytest 
