from tokenize import String

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, as_declarative

@as_declarative()
class SqlAlchemyBase:
    # Базовый класс для объектов User и Task
    pass

# переменная, которая хранит фабрику сессий базы данных
__factory = None


def global_init(db_file: String) -> None:
    """
    Функция используется для инициализации подключения к базе данных и фабрики сессий.
    """
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False' #Можно отредактировать, для использования с базами данных других типов
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """
    Функция возвращает новую сессию SQLAlchemy, созданную из глобальной фабрики сессий
    """
    global __factory
    return __factory()
