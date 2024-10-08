#!/bin/bash

# Step 1: Check if the tmp directory exists
if [ -d "tmp" ]; then
  # Step 2: If it does exist, delete it
  rm -rf tmp
fi

# Step 3: Create a tmp directory
mkdir tmp

# Step 4: Run a django-admin startproject command inside the tmp directory
pipenv run django-admin startproject \
    --template=. \
    --extension 'py,yaml,md,template,toml,json' \
    --name Makefile \
    --exclude '.ruff_cache' \
    tmp_project \
    tmp