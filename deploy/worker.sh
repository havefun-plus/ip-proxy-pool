#!/bin/bash

export CRONJOB_SETTINGS=ipfeeder.settings
export PYTHONPATH=.

exec cronjob run --mode distributed --node worker

