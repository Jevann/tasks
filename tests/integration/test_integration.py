import asyncpg
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'tasks_service/app'))
sys.path.append(str(BASE_DIR / 'bored_service/app'))

from tasks_service.app.main import service_alive as tasks_status
from bored_service.app.main import service_alive as bored_status


@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect('postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query')
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"


@pytest.mark.asyncio
async def test_tasks_service_connection():
    r = await tasks_status()
    assert r == {'message': 'Service alive'}


@pytest.mark.asyncio
async def test_bored_service_connection():
    r = await bored_status()
    assert r == {'message': 'Service alive'}
