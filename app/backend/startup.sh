#!/bin/bash
# Production startup with proper worker configuration
gunicorn --bind=0.0.0.0:8000 \
  --workers=2 \
  --threads=4 \
  --timeout=300 \
  --worker-class=gthread \
  --access-logfile=- \
  --error-logfile=- \
  --log-level=info \
  app:app

