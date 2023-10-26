from googleapiclient.discovery import build
import os

class APIMixin:
    """Класс-миксин для предоставления доступа к API."""

    __API_KEY: str = os.getenv('API_KEY')

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект для работы с API youtube."""
        service = build('youtube', 'v3', developerKey=cls.__API_KEY)
        return service
