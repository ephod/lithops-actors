# Lithops actors

Original repository: https://github.com/danielBCN/lithops-actors

## Installation

Create Python environment and upgrade pip to the latest version available.

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Production

```shell
python -m pip install -r requirements.txt
```

### Development

```shell
python -m pip install -r requirements-dev.txt
```

### Follow logs

```shell
lithops logs poll
```

## Docker compose

[Prometheus Redis Metrics Exporter](https://github.com/oliver006/redis_exporter)

### No SSL/TLS for Redis exporter

```yaml
  redis-exporter:
    image: oliver006/redis_exporter:v1.24.0-alpine
    command: -redis.addr ${REDIS_SCHEMA:-redis}://${REDIS_HOST}:${REDIS_PORT} -redis.password ${REDIS_PASSWORD}
    ports:
      - "127.0.0.1:9121:9121"
```

### SSL/TLS

```yaml
  redis-exporter:
    image: oliver006/redis_exporter:v1.24.0-alpine
    command: -redis.addr ${REDIS_SCHEMA:-rediss}://${REDIS_HOST}:${REDIS_PORT} -redis.password ${REDIS_PASSWORD}
    ports:
      - "127.0.0.1:9121:9121"
```
