import subprocess
import requests
import pytest

NGINX_URL = "http://localhost:80"
EXPECTED_BODY = "Hello from Effective Mobile!"


def test_nginx_returns_200():
    r = requests.get(NGINX_URL)
    assert r.status_code == 200


def test_nginx_returns_correct_body():
    r = requests.get(NGINX_URL)
    assert r.text == EXPECTED_BODY


def test_nginx_content_type_is_plain_text():
    r = requests.get(NGINX_URL)
    assert "text/plain" in r.headers.get("Content-Type", "")


def test_backend_not_exposed_on_host():
    import json
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{json .NetworkSettings.Ports}}", "em-backend"],
        capture_output=True,
        text=True,
        check=True,
    )
    ports = json.loads(result.stdout.strip())
    # null binding means port is declared via EXPOSE but not published to host
    for bindings in ports.values():
        assert bindings is None, "backend container must not publish any ports to the host"
