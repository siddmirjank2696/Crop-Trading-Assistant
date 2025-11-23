#!/bin/bash
# A script to execute the pipeline

# Pulling the latest models from GitHub
git pull

# Building the docker image
docker build -t "crop_assistant_img" .

# Running the docker image
docker run -p 8501:8501 crop_assistant_img