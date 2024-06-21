#!/bin/bash
source /root/APMproject/bin/activate
exec gunicorn  -c "/root/APMproject/APM/gunicorn_config.py" APM.wsgi
