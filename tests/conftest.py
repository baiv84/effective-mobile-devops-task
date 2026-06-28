import subprocess
import time
import requests
import pytest

COMPOSE_FILE = "docker-compose.yml"
NGINX_URL = "http://localhost:80"
MAX_WAIT = 30


def wait_for_nginx():
    deadline = time.time() + MAX_WAIT
    while time.time() < deadline:
        try:
            r = requests.get(NGINX_URL, timeout=2)
            if r.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError("nginx did not become ready in time")


@pytest.fixture(scope="session", autouse=True)
def docker_stack():
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d", "--build"],
        check=True,
    )
    wait_for_nginx()
    yield
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "down"],
        check=True,
    )
