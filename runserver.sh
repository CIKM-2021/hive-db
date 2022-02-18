#!/bin/bash

uvicorn --interface wsgi --host 0.0.0.0 --port 5000 --reload src.app:app
