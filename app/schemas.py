from pydantic import BaseModel

# Для корневого ответа
class ReadRoot(BaseModel):
    message: str  # для сообщения, которое будет возвращено в ответе

# Для информации о сервере
class ServerInfo(BaseModel):
    fastapi_version: str  # для версии FastAPI
    python_version: str  # для версии Python

# Для информации о клиенте
class ClientInfo(BaseModel):
    client_ip: str  # для IP-адреса клиента
    user_agent: str  # для строки User-Agent клиента

# Для информации о базе данных
class DatabaseInfo(BaseModel):
    database: str  # тип бд
    version: str  # версия бд
    user: str  # имя пользователя бд
    host: str  # хост бд
    port: str  # порта бд
    dbname: str  # имя бд
