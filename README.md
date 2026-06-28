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
├── tests/
│   ├── conftest.py
│   ├── test_integration.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Технологии

- Python 3.12 (`http.server`)
- Nginx (alpine)
- Docker / Docker Compose

## Демо

Приложение развёрнуто и доступно в интернете: https://app-sibpsa.ru/effmobile/

## Как запустить

Предварительно убедитесь, что в системе установлены [Docker](https://docs.docker.com/get-docker/) и Docker Compose.

```bash
git clone https://github.com/baiv84/effective-mobile-devops-task.git
cd effective-mobile-devops-task
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

## Интеграционные тесты

Тесты поднимают стек через `docker compose`, проверяют поведение системы и останавливают контейнеры после завершения.

Что проверяется:

| Тест | Описание |
|---|---|
| `test_nginx_returns_200` | nginx отвечает со статусом HTTP 200 |
| `test_nginx_returns_correct_body` | тело ответа — `Hello from Effective Mobile!` |
| `test_nginx_content_type_is_plain_text` | заголовок `Content-Type: text/plain` |
| `test_backend_not_exposed_on_host` | backend не опубликован на хост-порт |

### Запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt
pytest tests/ -v
```

## Остановить

```bash
docker compose down
```
