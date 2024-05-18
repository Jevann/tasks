import requests
from datetime import date

base_url = 'http://localhost:8000'
add_task_url = f'{base_url}/add_task'
get_tasks_url = f'{base_url}/tasks'
get_task_by_id_url = f'{base_url}/get_task_by_id'
delete_task_url = f'{base_url}/delete_task'

new_task = {
    "id": 99,
    "title": "Complete Assignment",
    "description": "Finish the mathematics assignment",
    "priority": 1,
    "due_date": str(date(2024, 6, 1))
}

def test_health_check():
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Service alive"}

def test_add_task():
    response = requests.post(add_task_url, json=new_task)
    assert response.status_code == 200
    assert response.json()['title'] == new_task['title']

def test_get_tasks():
    response = requests.get(get_tasks_url)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_task_by_id():
    response = requests.get(f"{get_task_by_id_url}/99")
    assert response.status_code == 200
    assert response.json()['title'] == new_task['title']

def test_delete_task():
    delete_response = requests.delete(f"{delete_task_url}/99")
    assert delete_response.status_code == 200
    response = requests.get(f"{get_task_by_id_url}/99")
    assert response.status_code == 404

