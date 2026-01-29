import pytest
import requests
import time

BASE_URL = "https://ru.yougile.com/api-v2"
TOKEN = "8PqO6ZHTVR1xeLMWqRAD7L6G1-N+oLoIQlZf59v2Xplpm7Wliz-07VivutLZwv7I"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def generate_unique_project_title():
    timestamp = str(int(time.time()))
    return f"Авто тесты {timestamp}"

def cleanup_project(project_id):
    if project_id:
        cleanup_url = f"{BASE_URL}/projects/{project_id}"
        cleanup_data = {"deleted": True}
        try:
            requests.put(cleanup_url, json=cleanup_data, headers=HEADERS)
        except Exception as e:
            print(f"Не удалось удалить проект {project_id}: {e}")

 ПОЗИТИВНЫЕ ТЕСТЫ 

@pytest.mark.positive
def test_create_project_post():
    """Позитивный тест POST: создание проекта с валидными данными."""
    project_title = generate_unique_project_title()
    payload = {"title": project_title}
    
    response = requests.post(
        f"{BASE_URL}/projects",
        json=payload,
        headers=HEADERS,
    )
    
    assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}. Ответ: {response.text}"
    
    response_data = response.json()
    assert isinstance(response_data.get("id"), str), "Ответ должен содержать ID в формате строки"
    assert response_data["id"], "ID проекта не должен быть пустым"

    project_id = response_data["id"]

    cleanup_project(project_id)

@pytest.mark.positive  
def test_get_project_by_id():

    project_title = generate_unique_project_title()
    create_payload = {"title": project_title}
    
    create_response = requests.post(
        f"{BASE_URL}/projects",
        json=create_payload,
        headers=HEADERS,
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/projects/{project_id}",
        headers=HEADERS,
    )

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    response_data = response.json()
    assert response_data["id"] == project_id, f"ID в ответе ({response_data['id']}) должен совпадать с запрошенным ({project_id})"
    assert response_data["title"] == project_title, "Название проекта должно совпадать"
    assert "timestamp" in response_data, "Ответ должен содержать поле timestamp"
    assert isinstance(response_data["timestamp"], (int, float)), "timestamp должен быть числом"

    cleanup_project(project_id)

@pytest.mark.positive
def test_update_project_put():
    """Позитивный тест PUT: обновление существующего проекта."""
    project_title = generate_unique_project_title()
    create_payload = {"title": project_title}
    
    create_response = requests.post(
        f"{BASE_URL}/projects",
        json=create_payload,
        headers=HEADERS,
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    new_title = f"Обновленный {project_title}"
    update_payload = {"title": new_title}
    
    response = requests.put(
        f"{BASE_URL}/projects/{project_id}",
        json=update_payload,
        headers=HEADERS,
    )

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    get_response = requests.get(
        f"{BASE_URL}/projects/{project_id}",
        headers=HEADERS,
    )
    updated_data = get_response.json()
    assert updated_data["title"] == new_title, f"Название должно обновиться на '{new_title}'"

    cleanup_project(project_id)

НЕГАТИВНЫЕ ТЕСТЫ 

@pytest.mark.negative
def test_create_project_post_invalid():

    payload = {}  # Пустой payload - нет обязательного поля title
    
    response = requests.post(
        f"{BASE_URL}/projects",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 400, f"Ожидался 400 для невалидных данных, получен {response.status_code}"

    response_data = response.json()
    assert "error" in response_data or "message" in response_data, "Ответ должен содержать информацию об ошибке"

@pytest.mark.negative
def test_get_nonexistent_project():

    non_existent_id = "non_existent_id_12345"
    
    response = requests.get(
        f"{BASE_URL}/projects/{non_existent_id}",
        headers=HEADERS,
    )
 
    assert response.status_code == 404, f"Ожидался 404 для несуществующего проекта, получен {response.status_code}"

    response_data = response.json()
    assert "error" in response_data or "message" in response_data, "Ответ должен содержать информацию об ошибке"

@pytest.mark.negative
def test_update_nonexistent_project():
    """Негативный тест PUT: попытка обновления несуществующего проекта."""

    non_existent_id = "non_existent_id_12345"
    update_payload = {"title": "Новое название"}
    
    response = requests.put(
        f"{BASE_URL}/projects/{non_existent_id}",
        json=update_payload,
        headers=HEADERS,
    )
    
    assert response.status_code == 404, f"Ожидался 404 для несуществующего проекта, получен {response.status_code}"
  
    response_data = response.json()
    assert "error" in response_data or "message" in response_data, "Ответ должен содержать информацию об ошибке"

@pytest.mark.negative
def test_create_project_with_empty_title():
    """Негативный тест POST: создание проекта с пустым названием."""
    payload = {"title": ""}  # Пустая строка вместо валидного названия
    
    response = requests.post(
        f"{BASE_URL}/projects",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code in [400, 422], f"Ожидалась ошибка валидации, получен {response.status_code}"

@pytest.mark.negative
def test_update_with_invalid_data():
    """Негативный тест PUT: обновление проекта с невалидными данными."""
    
    project_title = generate_unique_project_title()
    create_payload = {"title": project_title}
    
    create_response = requests.post(
        f"{BASE_URL}/projects",
        json=create_payload,
        headers=HEADERS,
    )
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]
    
    # Пытаемся обновить с невалидными данными (например, пустой title)
    invalid_payload = {"title": ""}
    
    response = requests.put(
        f"{BASE_URL}/projects/{project_id}",
        json=invalid_payload,
        headers=HEADERS,
    )
    

    assert response.status_code in [400, 422], f"Ожидалась ошибка валидации, получен {response.status_code}"
    
    cleanup_project(project_id)
