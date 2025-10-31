# Runbook - Stage 3 Observability

## Overview
This service monitors system metrics and sends data to AWS.

## Steps
1. Build Docker image:
   docker-compose build
2. Start services:
   docker-compose up -d
3. Check logs:
   docker-compose logs watcher
4. Stop services:
   docker-compose down
