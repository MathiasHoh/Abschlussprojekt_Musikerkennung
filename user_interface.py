import time
import os
from io import BytesIO

import streamlit as st
from googleapiclient.discovery import build

from recognise import Recogniser

recognised = list()

# Klasse für die Musikerkennung
class MusicRecognition:

    def __init__(self, recogniser: Recogniser):
        self.recogniser = recogniser
        self.song_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "songs"
        )
        if not os.path.exists(self.song_dir):
            os.mkdir(self.song_dir)

        self.show_music_recognition()

    def show_music_recognition(self):
        st.header('Musikerkennung')
        if st.button('Musik erkennen'):
            # Zeige das GIF und führe Musikerkennung durch
            placeholder = st.empty()
            placeholder.markdown("![Erkennung läuft](https://i.gifer.com/8IL.gif)")
           
            with st.spinner('Höre zu und erkenne...'):
                info = self.recogniser.listen_to_song()

            placeholder.empty()
            #erkennungserfolg=False
            if isinstance(info, tuple):
                artist, album, title = info
                recognised.append(info)
            
                spotify_link = f"https://open.spotify.com/search/{info[1][0].replace(' ', '')}+{info[1][1].replace(' ', '')}"
                st.write("Spotify Link:", spotify_link)
                st.success('Erkennung erfolgreich!')
                st.markdown("![Noice](https://i.gifer.com/Eh2.gif)")

                st.write(f"Interpret: {artist}") 
                st.write(f"Interpret: {title}") 
                st.write(f"Interpret: {album}")

            else:
                st.error('Kein Erfolg. Bitte versuch es nochmal')
                st.markdown("![Oh No!](https://i.gifer.com/20F5.gif)")

        st.write("Oder lade eine Musikdatei hoch, um sie zu erkennen.")
        uploaded_file = st.file_uploader("Ziehe eine Datei hierher oder klicke um eine Datei auszuwählen", type=['mp3', 'wav'])
        if uploaded_file is not None:
            with st.spinner('Erkenne Musik aus Datei...'):
                file_path = self.__save_fie(uploaded_file)
                info = self.recogniser.recognise_song(file_path)

            if isinstance(info, tuple):
                artist, album, title = info
                recognised.append(info)

                spotify_link = f"https://open.spotify.com/search/{info[1][0].replace(' ', '')}+{info[1][1].replace(' ', '')}"
                st.write("Spotify Link:", spotify_link)
                st.success('Erkennung erfolgreich!')
                st.markdown("![Noice](https://i.gifer.com/Eh2.gif)")

                st.write(f"Interpret: {artist}") 
                st.write(f"Interpret: {title}") 
                st.write(f"Interpret: {album}") 

            else:
                print(info)
                st.error('Kein Erfolg. Bitte versuch es nochmal')
                st.markdown("![Oh No!](https://i.gifer.com/20F5.gif)")
    
    def __save_fie(self, uploaded_file: BytesIO):
        path = os.path.join(
            self.song_dir,
            uploaded_file.name
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
        
        return path


class LibraryExtension:
    def __init__(self, recogniser: Recogniser):
        self.recogniser = recogniser
        self.song_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "songs"
        )
        if not os.path.exists(self.song_dir):
            os.mkdir(self.song_dir)

        self.show_library_extension()

    def show_library_extension(self):
        st.header('Bibliothek erweitern')

                # Eingabefelder für Interpret, Titel und Album
        interpret = st.text_input("Interpret", key="interpret_input")
        title = st.text_input("Titel", key="title_input")
        album = st.text_input("Album", key="album_input")

        uploaded_files = st.file_uploader("Ziehe Dateien hierher oder klicke, um Dateien auszuwählen", accept_multiple_files=True, type=['mp3', 'wav'], key="library_extension")

        with st.spinner('Lade Neues Lied in die Datenbank'):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                
                    file_path = self.__save_fie(uploaded_file)
                    self.recogniser.register_song(file_path)
                    st.write(f"Datei {uploaded_file.name} erfolgreich hochgeladen.")
    
    def __save_fie(self, uploaded_file: BytesIO):
        path = os.path.join(
            self.song_dir,
            uploaded_file.name
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
        
        return path


class RecognisedSongs:
    def __init__(self) -> None:
        st.header('Bibliothek erweitern')
        for artist, album, title in recognised:
            st.write(f"{title} - {artist} ({album})")

# Hauptklasse der Anwendung
class RhythmRadarApp:
    def __init__(self):
        self.recogniser = Recogniser()
        st.title('RhythmRadar')
        self.menu = st.sidebar.radio("Menü", ('Musikerkennung', 'Meine erkannten Songs', 'Bibliothek erweitern'))
        self.handle_menu()

    def handle_menu(self):
        if self.menu == 'Musikerkennung':
            MusicRecognition(self.recogniser)
        elif self.menu == 'Bibliothek erweitern':
            LibraryExtension(self.recogniser)
        elif self.menu == 'Meine erkannten Songs':
            RecognisedSongs()
        # Implementiere hier weitere elif-Blöcke für andere Menüpunkte

if __name__ == "__main__":
    RhythmRadarApp()
