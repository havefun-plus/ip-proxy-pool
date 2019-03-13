#!/bin/bash

export CRONJOB_SETTINGS=ipfeeder.settings
export PYTHONPATH=.

exec gunicorn -c deploy/gunicorn.conf.py ipfeeder.web.views:app
