import os
import json

from googleapiclient.discovery import build

class Video:
    api_key: str = os.getenv('API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        # print(json.dumps(video_response, indent=2, ensure_ascii=False))
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v=gaoc9MPZ4bw'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return str(f'{self.title} ({self.url})')

class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


# video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
# video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')