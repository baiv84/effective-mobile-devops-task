# Effective Mobile — тестовое задание DevOps

Простое веб-приложение, доступное через nginx (reverse proxy), оба сервиса запущены в Docker-контейнерах.

## Архитектура

```
   curl http://localhost
          │
          ▼
   ┌─────────────┐        docker-сеть em-network        ┌─────────────────┐
   │  em-nginx   │ ────── proxy_pass http://backend ───▶ │   em-backend    │
   │  :80 (host) │                                       │  :8080 (internal)│
   └─────────────┘                                       └─────────────────┘
```

- **nginx** слушает порт 80 и единственный опубликован на хост.
- **backend** — Python `http.server`, слушает порт 8080 только внутри docker-сети, с хоста недоступен.
- nginx проксирует все запросы на `/` в backend по имени сервиса (`backend:8080`) и передаёт заголовки `Host`, `X-Real-IP`, `X-Forwarded-For`.

## Структура проекта

```
├── backend/
│   ├── Dockerfile
│   └── app.py
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Технологии

- Python 3.12 (`http.server`)
- Nginx (alpine)
- Docker / Docker Compose

## Как запустить

```bash
docker compose up -d --build
```

## Как проверить результат

```bash
curl http://localhost
```

Ожидаемый ответ:

```
Hello from Effective Mobile!
```

Убедиться, что backend не доступен с хоста напрямую:

```bash
curl http://localhost:8080   # должно завершиться ошибкой соединения
```

## Остановить

```bash
docker compose down
```
