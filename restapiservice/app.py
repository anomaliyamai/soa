import db
from fastapi import FastAPI, HTTPException
from typing import Union
from pydantic import BaseModel
import uvicorn
import psycopg2


class User(BaseModel):
    name: Union[str, None] = None
    surname: Union[str, None] = None
    birth_date: Union[str, None] = None
    email: Union[str, None] = None
    phone_number: Union[str, None] = None
    login: str
    password: str


app = FastAPI()
alchemy_instance = db.Executor("postgresql+psycopg2://postgres:password@db:5432/postgres")


@app.post("/registrate")
def create_user(user_data: User):
    alchemy_instance.create_user([user_data.login, user_data.password])


@app.post("/authorize")
def authorize(user_data: User):
    if not alchemy_instance.user_exists([user_data.login, user_data.password]):
        raise HTTPException(status_code=404, detail="Password or login missing in system")
    alchemy_instance.set_session_id([user_data.login, user_data.password])


@app.put("/update")
def update(user_data: User):
    alchemy_instance.update_user([user_data.login, user_data.password, user_data.name, user_data.surname,
                                  user_data.birth_date, user_data.email, user_data.phone_number])


if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
