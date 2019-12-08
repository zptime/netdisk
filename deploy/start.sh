#!/usr/bin/env bash
. /opt/virt/netdisk/bin/activate
cd ..
gunicorn --config gunicorn.conf netdisk.wsgi:application --daemon

