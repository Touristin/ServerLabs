from sqlalchemy import create_engine  # Импорт функции для соединения с бд
from sqlalchemy.ext.declarative import declarative_base # базовый класс для моделей
from sqlalchemy.orm import sessionmaker  # Импорт класса для создания фабрики сессий

# Строка подключения к базе данных
DATABASE_URL = "postgresql://turistin:1234@localhost:5432/postgres"

# Создание движка SQLAlchemy
# Движок управляет подключением к базе данных и выполняет SQL-запросы
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()
