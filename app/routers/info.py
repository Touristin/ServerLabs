from fastapi import APIRouter, Request  # Импорт APIRouter для создания маршрутизатора и Request для получения информации о запросе
from sqlalchemy.exc import SQLAlchemyError  # Импорт для обработки ошибок SQLAlchemy
from sqlalchemy.sql import text  # Для выполнения SQL-запросов в виде текста
from ..database import engine, DATABASE_URL  # Импорт соединения с БД (engine) и строки подключения (DATABASE_URL)
from ..schemas import *  # Импорт Pydantic моделей
import fastapi  # Импорт модуля FastAPI для получения версии
import sys  # Для получения версии Python
import re  # Модуль регулярных выражений для обработки строки подключения к БД

# Создание экземпляра маршрута
router = APIRouter()

@router.get("/info/server", response_model=ServerInfo)
def get_server_info():
    """
    Получить информацию о сервере.

    Возвращает JSON-объект с версией FastAPI и версией Python,
    на которых запущено приложение.
    """
    return {
        "fastapi_version": fastapi.__version__,  # Текущая версия FastAPI
        "python_version": sys.version  # Текущая версия Python
    }

@router.get("/info/client", response_model=ClientInfo)
def get_client_info(request: Request):
    client_ip = request.client.host  # Получение IP-адреса клиента
    user_agent = request.headers.get("user-agent")  # Получение User-Agent
    return {"client_ip": client_ip, "user_agent": user_agent}

@router.get("/info/database", response_model=DatabaseInfo)
def get_database_info():
    try:
        # Подключение к базе данных
        connection = engine.connect()

        # Выполнение запроса для получения версии бд
        result = connection.execute(text("SELECT version();"))
        db_version = result.fetchone()  # Получение результата запроса

        # Извлечение информации из строки подключения с использованием регулярного выражения
        match = re.match(
            r'postgresql://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:/]+)(?::(?P<port>\d+))?/(?P<dbname>[^?]+)', 
            DATABASE_URL
        )
        if match:
            user = match.group('user')  # Имя пользователя
            host = match.group('host')  # Хост бд
            port = match.group('port')  # Порт подключения
            dbname = match.group('dbname')  # Название бд
        else:
            # Если строка подключения не соответствует шаблону
            user = host = port = dbname = "Unknown"

        connection.close()  # Закрытие соединения
        return {
            "database": "PostgreSQL",  # Тип бд
            "version": db_version[0],  # Версия бд
            "user": user,  # Имя пользователя
            "host": host,  # Хост
            "port": port,  # Порт
            "dbname": dbname  # Название бд
        }
    except SQLAlchemyError as e:
        # Обработка ошибок SQLAlchemy и возврат сообщения об ошибке
        return {"error": str(e)}
