FROM python:3.11-slim

LABEL maintainer="TeamMavericKX"
LABEL project="Mastery Decision Engine"
LABEL version="1.0"

WORKDIR /app

COPY tools/ ./tools/

CMD ["python", "tools/mastery_engine.py"]
