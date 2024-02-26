import streamlit as st
import time
from googleapiclient.discovery import build
#Api-Key
api_key = "AIzaSyBhALmgY9R3oeszHGvGKAGNjAGGBmMM6N8"
#Youtube Funktion
def get_youtube_charts(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="DE",
        videoCategoryId="10",
        maxResults=10
    )
    response = request.execute()
    return response

# Menüauswahl im Sidebar für Nutzerverwaltung
user_management = st.sidebar.radio("Nutzer Verwaltung", ('Anmelden', 'Als Gast fortfahren'))

if user_management == 'Anmelden':
    # Anmeldeformular
    st.sidebar.header('Anmeldung')
    username = st.sidebar.text_input("Benutzername")
    password = st.sidebar.text_input("Passwort", type='password')
    login_button = st.sidebar.button('Anmelden')

    if login_button:
        
        if username == "admin" and password == "password":
            st.sidebar.success('Erfolgreich angemeldet.')
            # Weiterleitung oder Freischaltung der Hauptfunktionen der App
        else:
            st.sidebar.error('Anmeldung fehlgeschlagen.')

elif user_management == 'Als Gast fortfahren':
    
    st.sidebar.success('Du fährst als Gast fort.')

# Haupttitel der Seite
st.title('RhythmRadar')

# Menüauswahl
menu = st.sidebar.radio("Menü", ('Musikerkennung', 'Meine erkannten Songs', 'Bibliothek', 'YouTube-Charts', 'Bibliothek erweitern'))

# Musikerkennung
if menu == 'Musikerkennung':
    st.header('Musikerkennung')
    st.write('Drücke den Button unten, um mit der Musikerkennung zu starten.')
    
    if st.button('Musik erkennen'):
        # Zeige das GIF direkt nach Button-Klick an
        st.markdown(
            """
            <img src="loading.gif" alt="Loading" style="width:100px;height:100px;">
            """,
            unsafe_allow_html=True
        )
        
        # Verwende den Spinner für die simulierte Wartezeit
        with st.spinner('Höre zu und erkenne...'):
            ### Hier Musikerkennungsfunktion
            ### Nur zum Probieren, wenn fertig, entfernen von hier
            time.sleep(5)  # Simulierte Wartezeit
            ### bis hier
        
        
        
        #Wenn erfolgreich
        erkennungserfolg = True
        if erkennungserfolg:
            st.success('Erkennung erfolgreich!')
            st.write('') ### Hier Künstler oder Titel
            st.write('') ##  Hier Titel oder Künstler
            
        else:
            st.error('Keine Musik erkannt. Bitte versuche es erneut.')
    st.write("Oder lade eine Musikdatei hoch, um sie zu erkennen.")
    
    # Datei-Uploader für Musikerkennung
    uploaded_file = st.file_uploader("Ziehe eine Datei hierher oder klicke um eine Datei auszuwählen", type=['mp3', 'wav'])
    if uploaded_file is not None:
        with st.spinner('Erkenne Musik aus Datei...'):
            ### Hier Musikerkennungsfunktion mit `uploaded_file`
            
        # Wenn erfolgreich
            erkennungserfolg = True
        if erkennungserfolg:
            st.success('Dateierkennung erfolgreich!')
            st.write('') ### Hier Künstler oder Titel aus der Datei
            st.write('') ##  Hier Titel oder Künstler aus der Datei
            
        else:
            st.error('Keine Musik aus Datei erkannt. Bitte versuche es erneut oder wähle eine andere Datei.')            
elif menu == 'Meine erkannten Songs':
    # Erkannte Songs
    st.header('Meine erkannten Songs')
    st.write('Liste der erkannten Songs...')
    ### Hier Datenbank von Verlauf

elif menu == 'Bibliothek':
    # Bibliothek
    st.header('Bibliothek')
    st.write('Anzeige der Musikbibliothek...')
    ### Hier Datenbank der Bibliothek
elif menu == 'Bibliothek erweitern':
    # Bibliothek erweitern
    st.header('Bibliothek erweitern')
    uploaded_file = st.file_uploader("Wähle eine Datei aus")
    if uploaded_file is not None:
        ### Hier funktion zum hinzufügen zur Datenbank
        st.write("Datei erfolgreich hochgeladen.")

#Hier Code für Reiter Youtube
elif menu == 'YouTube-Charts':
    st.header('YouTube Top Musikvideos')
    
    # YouTube-Charts holen
    charts_button = st.button('Lade YouTube Top Musikvideos')
    if charts_button:
        with st.spinner('Lade YouTube Top Musikvideos...'):
            charts = get_youtube_charts(api_key)
            for video in charts.get('items', []):
                video_title = video['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                st.markdown(f"[{video_title}]({video_url})")
