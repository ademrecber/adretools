#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python adretools/manage.py collectstatic --noinput
python adretools/manage.py migrate