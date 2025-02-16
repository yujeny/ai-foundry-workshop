#!/bin/bash
export PORT=8002
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
