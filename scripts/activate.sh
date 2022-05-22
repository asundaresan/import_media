#!/bin/bash 

# get default virtualenv folder name
version=`python3 -c "import platform; print(platform.python_version())"`
folder=venv/`hostname -s`_${version}

# if virtualenv is not installed, install and update it
if [[ ! -f ${folder}/bin/activate ]]; then
  python3 -m venv ${folder}
  echo "Please run the following to update to latest: "
  echo python -m pip install -U pip setuptools wheel
fi

source ${folder}/bin/activate

