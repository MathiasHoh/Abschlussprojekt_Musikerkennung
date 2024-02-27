import streamlit as st
import time
from googleapiclient.discovery import build


# Klasse für die Musikerkennung
class MusicRecognition:
    def __init__(self):
        self.show_music_recognition()

    def show_music_recognition(self):
        st.header('Musikerkennung')
        # Implementiere die Logik für Musikerkennung

# Klasse für YouTube-Charts
class YouTubeCharts:
    def __init__(self, api_key):
        self.api_key = api_key
        self.show_youtube_charts()

    def get_youtube_charts(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode="DE",
            videoCategoryId="10",
            maxResults=10
        )
        response = request.execute()
        return response

    def show_youtube_charts(self):
        st.header('YouTube Top Musikvideos')
        charts_button = st.button('Lade YouTube Top Musikvideos')
        if charts_button:
            with st.spinner('Lade YouTube Top Musikvideos...'):
                charts = self.get_youtube_charts()
                for video in charts.get('items', []):
                    video_title = video['snippet']['title']
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                    st.markdown(f"[{video_title}]({video_url})")

# Hauptklasse der Anwendung
class RhythmRadarApp:
    def __init__(self, api_key):
        self.api_key = api_key
        st.title('RhythmRadar')
        UserManagement()
        self.menu = st.sidebar.radio("Menü", ('Musikerkennung', 'Meine erkannten Songs', 'Bibliothek', 'YouTube-Charts', 'Bibliothek erweitern'))
        self.handle_menu()

    def handle_menu(self):
        if self.menu == 'Musikerkennung':
            MusicRecognition()
        elif self.menu == 'YouTube-Charts':
            YouTubeCharts(self.api_key)
        # Füge hier weitere elif-Blöcke für andere Menüpunkte hinzu

if __name__ == "__main__":
    api_key = "AIzaSyBhALmgY9R3oeszHGvGKAGNjAGGBmMM6N8"
    RhythmRadarApp(api_key)
