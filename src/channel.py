import json
import os

from src.apimixin import APIMixin


class Channel(APIMixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = ''.join(['https://www.youtube.com/channel/', self.channel_id])
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']


    def __str__(self):
        """Возвращает название и ссылку канала"""
        return str(f'{self.title} ({self.url})')

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __lt__(self, other):
        return int(other.subscriberCount) < int(self.subscriberCount)

    def __le__(self, other):
        return int(other.subscriberCount) <= int(self.subscriberCount)

    def __gt__(self, other):
        return int(other.subscriberCount) > int(self.subscriberCount)

    def __eq__(self, other):
        return int(other.subscriberCount) == int(self.subscriberCount)

    def to_json(self, filename):
        with open(file=filename, mode='w', encoding='utf-8') as f:
            json.dump(self.channel, f, indent=4, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
