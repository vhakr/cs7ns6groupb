#!/bin/bash
app-start-all-nodes
. /app/venv/bin/activate && web-server-entrypoint.sh
app-stop-all-nodes
