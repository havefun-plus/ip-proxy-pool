#!/bin/bash

export FLASK_APP=ipfeeder/web/views.py
export CRONJOB_SETTINGS=ipfeeder.settings
export PYTHONPATH=.

exec flask run

