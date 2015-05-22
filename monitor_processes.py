#!/usr/bin/env python

from datetime import datetime
import json
import psutil


def is_monitored_process(proc):
    try:
        return 'python' in proc.exe()
    except:
        return False  # permission denied, likely


def serialize_proc(proc):
    row = proc.as_dict()
    row['_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for key, value in row.iteritems():
        if isinstance(value, tuple) and hasattr(value, '_fields'):
            row[key] = dict(zip(value._fields, value))
    return row


for proc in psutil.process_iter():
    if is_monitored_process(proc):
        try:
            data = json.dumps(serialize_proc(proc))
            print(data)
        except:
            print({'error': 'Error reading {}'.format(proc.pid)})
            raise
