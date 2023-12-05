#!/bin/bash
set -o errexit

ruta=$(pwd) # Establece la ruta actual

if [ ! -d "env" ]; then # verifica la existencia del entorno virtual
    python3.11 -m virtualenv env
fi
if [ ! -d "logs" ]; then
    mkdir -p $ruta/logs
fi


$ruta/env/bin/python -m pip install -r $ruta/requirements.txt
$ruta/env/bin/python $ruta/manage.py migrate
$ruta/env/bin/python $ruta/manage.py collectstatic --no-input

yarn --cwd $ruta/static/css
yarn --cwd $ruta/static/css tailwindcss -i styles.css -o compiled.css
