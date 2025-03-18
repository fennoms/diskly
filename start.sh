#!/bin/bash

echo "Starting Diskly...\n"
docker build --no-cache -t diskly .; docker run diskly
