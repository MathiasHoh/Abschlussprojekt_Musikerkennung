import os
import sys
from io import BytesIO
import wave
from urllib.parse import quote, quote_plus

import streamlit as st

import numpy as np
import matplotlib.pyplot as plt


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
            if isinstance(info, tuple):
                artist, album, title = info
                recognised.append(info)
            
                spotify_link = f"https://open.spotify.com/search/{quote(f'{artist} {title}')}"
                youtube_link = f"https://www.youtube.com/results?search_query={quote_plus(f'{artist} {title}')}"
                st.success('Erkennung erfolgreich!')
                st.write(f"{title} - {artist} ({album})")
                st.link_button("Mit Spotify öffnen", spotify_link)
                st.link_button("Mit Youtube öffnen", youtube_link)

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

                spotify_link = f"https://open.spotify.com/search/{quote(f'{artist} {title}')}"
                youtube_link = f"https://www.youtube.com/results?search_query={quote_plus(f'{artist} {title}')}"
                st.success('Erkennung erfolgreich!')
                st.write(f"{title} - {artist} ({album})")
                st.link_button("Mit Spotify öffnen", spotify_link)
                st.link_button("Mit Youtube öffnen", youtube_link)

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

        uploaded_file = st.file_uploader("Ziehe Dateien hierher oder klicke, um Dateien auszuwählen", accept_multiple_files=False, type=['mp3', 'wav'], key="library_extension")

        with st.spinner('Lade Neues Lied in die Datenbank'):
            if uploaded_file:
                file_path = self.__save_fie(uploaded_file)
                self.recogniser.register_song(file_path, interpret=interpret, album=album, title=title)
                st.write(f"Datei {uploaded_file.name} erfolgreich hochgeladen.")   

                audio_bytes = uploaded_file.getvalue()
                st.audio(audio_bytes, format='audio/wav')

                with wave.open(file_path, "rb") as spf:
                    # Extrahiere das Raw-Audio aus der Wav-Datei
                    signal = spf.readframes(-1)
                    signal = np.frombuffer(signal, dtype=np.int16)

                    # Wenn Stereo
                    if spf.getnchannels() == 2:
                        st.write("Just mono files")
                        sys.exit(0)

                    fig, ax = plt.subplots()  # Erstelle eine Matplotlib-Figur und Achse
                    ax.plot(signal)  # Plotte das Audiosignal auf der Achse
                    plt.title("Signal Form")
                    st.pyplot(fig)



    def __save_fie(self, uploaded_file: BytesIO):
        path = os.path.join(
            self.song_dir,
            uploaded_file.name
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
        
        return path


class RecognisedSongs:
    def __init__(self, recogniser: Recogniser):

        st.header('Meine erkannten Songs')
        recognised = recogniser.get_history()
        print(recognised)
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
            RecognisedSongs(self.recogniser)
        # Implementiere hier weitere elif-Blöcke für andere Menüpunkte

if __name__ == "__main__":
    RhythmRadarApp()
