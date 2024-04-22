FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install . && \
    chmod +x ./docker-entrypoint.sh