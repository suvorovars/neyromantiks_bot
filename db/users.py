from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    """
    Объект таблицы users, в которой хранится:
    id - номер пользователя
    id_social_network - id пользователя в соц.сети
    name - имя пользователя
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_social_network: Mapped[str] = mapped_column(unique=True, nullable=False)

    name: Mapped[str] = mapped_column()
    tasks = relationship("Task", back_populates="user")

