#!/usr/bin/env bash

docker build -t financial_assistant .
docker run -p 3000:3000 --init financial_assistant