import os
import pytest
import uuid
import time
from typing import Generator, Dict, Any
from src.api.yougile_client import YougileClient

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: тесты, требующие подключения к API YouGile"
    )


@pytest.fixture(scope="session")
def api_token() -> str:
    token = os.getenv("YOUNGILE_API_TOKEN")
    if not token:
        pytest.skip("Нужна переменная YOUNGILE_API_TOKEN")
    return token


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("YOUNGILE_BASE_URL", "https://ru.yougile.com")


@pytest.fixture(scope="session")
def api_client(api_token: str, api_base_url: str) -> YougileClient:
    return YougileClient(base_url=api_base_url, api_token=api_token)


@pytest.fixture
def unique_prefix() -> str:
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())[:8]
    return f"test_{timestamp}_{unique_id}"


@pytest.fixture
def test_project_data(unique_prefix: str) -> Dict[str, Any]:
    return {
        "title": f"{unique_prefix}_project",
        "description": f"Тестовый проект {unique_prefix}"
    }


@pytest.fixture
def create_test_project(
    api_client: YougileClient, 
    test_project_data: Dict[str, Any]
) -> Generator[str, None, None]:
    response = api_client.create_project(
        title=test_project_data["title"],
        description=test_project_data.get("description")
    )
    
    assert response.status_code == 201, f"Ошибка {response.text}"
    
    project_id = response.json()["id"]
    
    yield project_id
  
    try:
        api_client.update_project(
            project_id=project_id,
            deleted=True
        )
    except Exception as e:
        print(f"Ошибка {project_id}: {e}")
