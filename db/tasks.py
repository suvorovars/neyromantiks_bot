from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    """
    ОбЪект таблицы tasks, в которой хранится
    id - номер задачи
    user_id - ссылка на номер пользователя из таблицы users
    task - Сама задача
    files - ссылки на файлы, приложенные к задаче
    """
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tasks")

    task: Mapped[str] = mapped_column(nullable=False)
    files: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default="В обработке у администратора")



