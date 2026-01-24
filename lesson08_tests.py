import pytest


# Позитивные проверки

@pytest.mark.integration
def test_positive_create_project_with_required_fields(
    api_client, 
    unique_prefix
):
    """Создание проекта с валидными полями."""
    project_title = f"{unique_prefix}_required_only"
    
    response = api_client.create_project(title=project_title)
  
    assert response.status_code == 201, \
        f"Ожидаемый результат статус: 201, фактический результат статус: {response.status_code}. Полученный ответ: {response.text}"
    
    response_data = response.json()
    assert "id" in response_data, 
    assert isinstance(response_data["id"], str), 
    assert len(response_data["id"]) > 0, 
    
    api_client.update_project(project_id=response_data["id"], deleted=True)


@pytest.mark.integration
def test_positive_create_project_with_all_fields(
    api_client, 
    unique_prefix
):
    """Создание проекта с наличием всех полей."""
    project_title = f"{unique_prefix}_full_project"
    project_description = f"Описание проекта {unique_prefix}"
    test_users = {}  
    
    response = api_client.create_project(
        title=project_title,
        description=project_description,
        users=test_users
    )
    
    assert response.status_code == 201, \
        f"Ожидаемый результат статус: 201, фактический результат статус: {response.status_code}"
    
    response_data = response.json()
    project_id = response_data["id"]
    
    get_response = api_client.get_project(project_id)
    assert get_response.status_code == 200
    
    project_data = get_response.json()
    assert project_data["title"] == project_title
    assert project_data.get("description") == project_description
    
    api_client.update_project(project_id=project_id, deleted=True)


@pytest.mark.integration
def test_positive_get_project(api_client, create_test_project):
    """Информация о проекте."""
    project_id = create_test_project
    
    response = api_client.get_project(project_id)
    
    assert response.status_code == 200, \
        f"Ожидаемый результат статус: 200, фактический результат статус: {response.status_code}"
    
    project_data = response.json()
    
    assert "id" in project_data,
    assert project_data["id"] == project_id, 
    assert "title" in project_data, 
    assert isinstance(project_data["title"], str), 
    assert "timestamp" in project_data, 
    assert isinstance(project_data["timestamp"], int), 


@pytest.mark.integration
def test_positive_update_project_title(api_client, create_test_project, unique_prefix):
    """Изменение названия проекта."""
    project_id = create_test_project
    new_title = f"{unique_prefix}_updated_title"
    
    response = api_client.update_project(project_id=project_id, title=new_title)
    
    assert response.status_code == 200, \
        f"Ожидаемый результат статус: 200, фактический результат статус: {response.status_code}"
    
    get_response = api_client.get_project(project_id)
    project_data = get_response.json()
    
    assert project_data["title"] == new_title, \
        f"Обновленное название: '{new_title}', фактическое: '{project_data.get('title')}'"


@pytest.mark.integration
def test_positive_update_project_description(api_client, create_test_project):
    """Обновление описания проекта."""
    project_id = create_test_project
    new_description = "Новое название крутое"
    response = api_client.update_project(
        project_id=project_id, 
        description=new_description
    )
    
    assert response.status_code == 200, \
        f"Ожидаемый результат статус: 200, фактический результат статус: {response.status_code}"
    
    get_response = api_client.get_project(project_id)
    project_data = get_response.json()
    
    assert project_data.get("description") == new_description, \


# Негативные тесты

@pytest.mark.integration
def test_negative_create_project_without_title(api_client):
    """Проект без названия."""
    response = api_client._send_request(
        method="POST",
        endpoint="/api-v2/projects",
        json={}  
    )
    
    assert response.status_code == 400, \
        f"Ожидаемый результат статус: 400, фактический результат статус: {response.status_code}"
    
    response_data = response.json()
    assert "error" in response_data or "message" in response_data, \



@pytest.mark.integration
def test_negative_create_project_with_empty_title(api_client):
    """Проект с пустым названием"""
    response = api_client.create_project(title="")
    и
    assert response.status_code in [400, 422], \
        f"Ожидаемый результат статус: 400 или 422, фактический результат статус: {response.status_code}"


@pytest.mark.integration
def test_negative_get_nonexistent_project(api_client):
    """Получение несуществующего проекта."""
    non_existent_id = "non_existent_project_12345"
    
    response = api_client.get_project(non_existent_id)
    
    assert response.status_code == 404, \
        f"Ожидаемый результат статус: 404, фактический результат статус: {response.status_code}"
    
    response_data = response.json()
    assert "error" in response_data or "message" in response_data, \


@pytest.mark.integration
def test_negative_update_nonexistent_project(api_client, unique_prefix):
    """Обновление несуществующего проекта."""
    non_existent_id = "non_existent_project_12345"
    new_title = f"{unique_prefix}_new_title"
    
    response = api_client.update_project(
        project_id=non_existent_id,
        title=new_title
    )
    
    assert response.status_code == 404, \
        f"Ожидаемый результат статус: 404, фактический результат статус: {response.status_code}"
    
    response_data = response.json()
    assert "error" in response_data, "Ответ должен содержать поле error"


@pytest.mark.integration
def test_negative_update_with_invalid_data(api_client, create_test_project):
    """Обновление невалидного проекта."""
    project_id = create_test_project
    
    response = api_client.update_project(project_id=project_id, title="")
    
    assert response.status_code in [400, 422], \
        f"ООжидаемый результат статус: 400 или 422, фактический результат статус: {response.status_code}}"


@pytest.mark.integration
def test_negative_unauthorized_request():
    """Запрос без авторизации."""
    from src.api.yougile_client import YougileClient
    
    client = YougileClient(
        base_url="https://ru.yougile.com",
        api_token="invalid_token_12345"
    )
    
    response = client.create_project(title="Тестовый проект")
    
    assert response.status_code in [401, 403], \
        f"Ожидаемый результат статус: 401 или 403, фактический результат статус: {response.status_code}}"
