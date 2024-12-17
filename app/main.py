from fastapi import FastAPI
from .routers import info
from .schemas import ReadRoot

# Создание экземпляра приложения FastAPI
app = FastAPI()

# Подключение маршрутизатора из модуля "info"
app.include_router(info.router)

@app.get("/", response_model=ReadRoot)
def read_root():
    """
    Корневой маршрут приложения.
    """
    return {
        "message": "Welcome to my FastAPI project | Разработка серверных приложений"
    }
