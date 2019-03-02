#!/bin/bash

export CRONJOB_SETTINGS=ipfeeder.settings
export PYTHONPATH=.

exec gunicorn -c gunicorn.conf.py ipfeeder.web.views:app
