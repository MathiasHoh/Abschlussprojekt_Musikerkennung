import streamlit as st
import time

###import funktion für Musikerkennung

# Haupttitel der Seite
st.title('RhythmRadar')

# Menüauswahl
menu = st.sidebar.radio("Menü", ('Musikerkennung', 'Meine erkannten Songs', 'Bibliothek', 'Bibliothek erweitern'))

if menu == 'Musikerkennung':
    # Musikerkennung
    st.header('Musikerkennung')
    st.write('Drücke den Button unten, um mit der Musikerkennung zu starten.')
    if st.button('Musik erkennen'):
        with st.spinner('Höre zu und erkenne...'):
            ### Hier Musikerkennungsfunktion 
            ###Nur zum probieren wenn fertig entfernen von hier
            time.sleep(5)  # Simulierte Wartezeit
            ###bis hier
        # Wenn erolgreich
        erkennungserfolg = True
        if erkennungserfolg:
            st.success('Erkennung erfolgreich!')
            st.write('') ### Hier Künstler oder Titel
            st.write('') ##  Hier Titel oder Künstler
            
        else:
            st.error('Keine Musik erkannt. Bitte versuche es erneut.')
    st.write("Oder lade eine Musikdatei hoch, um sie zu erkennen.")
    
    # Datei-Uploader für Musikerkennung
    uploaded_file = st.file_uploader("Ziehe eine Datei hierher oder klicke, um eine Datei auszuwählen", type=['mp3', 'wav'])
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
