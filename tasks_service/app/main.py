import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from sqlalchemy.orm import Session
from typing import List, Annotated
from tasks_model.model import Task
from tasks_database.database import TaskDB, SessionLocal
from keycloak import KeycloakOpenID

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def check_for_role(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (check_for_role(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_task", response_model=Task)
async def add_task(task: Task, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        new_task = TaskDB(**task.dict())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    else:
        return "Wrong JWT Token"


@app.get("/tasks", response_model=List[Task])
async def list_tasks(db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        return db.query(TaskDB).all()
    else:
        return "Wrong JWT Token"


@app.get("/get_task_by_id/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    else:
        return "Wrong JWT Token"


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: int, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
