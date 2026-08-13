#! /bin/bash

# Create env file
touch .env
echo $TEST_ENV > .env
source .env

# Run curl commands
curl --verbose --header "API-Key: $API_KEY_1" https://prometheus.io
curl --verbose --header "API-Key: $API_KEY_2" https://prometheus.io