#!/bin/bash

# Define the maximum number of instances
MAX_INSTANCES=5

# Count the number of instances running
RUNNING_INSTANCES=$(ps aux | grep '[m]pi_spawner.py' | wc -l)

# Check if the number of instances is less than the maximum
if [ "$RUNNING_INSTANCES" -lt "$MAX_INSTANCES" ]; then
    echo $RUNNING_INSTANCES
    # Start additional instances
    for ((i = 0; i < $((MAX_INSTANCES - RUNNING_INSTANCES)); i++)); do
       /bata/venv/bin/python3 /bata/src/cleanCopy/components/execution/mpi_spawner.py >/dev/null 2>&1 &
    done    
fi
