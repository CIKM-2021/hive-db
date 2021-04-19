#!/bin/bash

# gunicorn -b 0.0.0.0:8001 --reload src.app
uvicorn --interface wsgi --host 0.0.0.0 --port 8001 -v --reload src.app:app
