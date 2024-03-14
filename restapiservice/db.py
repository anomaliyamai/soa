from typing import Annotated, Optional, List
from sqlalchemy import VARCHAR, create_engine, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import uuid

int_pk = Annotated[int, mapped_column(primary_key=True)]
text_not_null = Annotated[str, mapped_column(VARCHAR())]
text = Annotated[Optional[str], mapped_column(VARCHAR())]


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    session: Mapped[Optional[uuid.UUID]]
    name: Mapped[text]
    surname: Mapped[text]
    birth_date: Mapped[text]
    email: Mapped[text]
    phone_number: Mapped[text]
    login: Mapped[text_not_null]
    password: Mapped[text_not_null]


class Executor:
    def __init__(self, engine_config: str) -> None:
        self.engine = create_engine(engine_config)
        Base.metadata.create_all(self.engine)

    def create_user(self, params: list[str]) -> None:
        with Session(self.engine) as session:
            new_user = Users(login=params[0], password=params[1])
            session.add(new_user)
            session.commit()

    def user_exists(self, params: list[str]) -> bool:
        with Session(self.engine) as session:
            resulting_rows = session.scalars(select(Users).where(Users.login == params[0] and Users.password == params[1])).all()
            session.commit()
        return len(resulting_rows) > 0

    def set_session_id(self, params: list[str]) -> None:
        with Session(self.engine) as session:
            session.execute(update(Users).where(Users.login == params[0] and Users.password == params[1]).values(session=uuid.uuid4()))
            session.commit()

    def update_user(self, params: list[str]) -> None:
        with Session(self.engine) as session:
            session.execute(update(Users).where(Users.login == params[0] and Users.password == params[1]).values(
                name=params[2], surname=params[3], birth_date=params[4], email=params[5], phone_number=params[6]))
            session.commit()


