FROM python:3.12-slim

WORKDIR /app

COPY app.py .

RUN useradd --no-create-home --shell /usr/sbin/nologin appuser
USER appuser

EXPOSE 8080

CMD ["python3", "app.py"]
