
import streamlit as st

# Haupttitel der Seite
st.title('RhythmRadar')

# Startseite
st.header('Willkommen bei RhythmRadar')
st.write('Drücke den Button unten, um mit der Musikerkennung zu starten.')

# Wenn der Button gedrückt wird
if st.button('Musik erkennen'):
    ### Hier Funktion zur SmallDickEnergy Musikerkennung aufrufen
    
    with st.spinner('Höre zu und erkenne...'):
        #Nur zum probieren wenn fertig entfernen von hier
        import time
        time.sleep(5)  # Simulierte Wartezeit
        # bis hier
        # Wenn erolgreich
        erkennungserfolg = True
        if erkennungserfolg:
            st.success('Erkennung erfolgreich!')
            st.write('') ### Hier Künstler oder Titel
            st.write('') ##  Hier Titel oder Künstler
            
        else:
            st.error('Keine Musik erkannt. Bitte versuche es erneut.')

# Erkannte Songs 
st.sidebar.title('Meine erkannten Songs')
## Hier eine Datenbank der erkannten Musik erstellen
st.write('- Beispiel-Song von Beispiel-Künstler')

