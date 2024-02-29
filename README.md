# Abschlussprojekt_Musikerkennung

# Installation
Damit das Programm funktioniert, müssen alle packages aus dem "requirements.txt" file installiert werden mit dem Befehl "pip install -r requirements.txt". Anschließend kann die Website mit dem Befehl "streamlit run user_interface.py", welcher in einen Terminal geschrieben werden muss, geöffnet werden.

# Problem bei der Installation

Falls es zu einem Fehler beim Installieren von einem der Pakete in "requirements.txt" kommt, so muss dieses Paket händisch im Terminal mit dem Befehl "pip install 'name des Pakets welches im Error genannt wird´" installiert und aus dem "requirements.txt" Dokument gelöscht werden. Anschließend muss das veränderte "requirements.txt" Dokument gespeichert werden und erneut mit dem Befehl "pip install -r requirements.txt" ausgeführt werden.

# Beschreibung der Funktionalität des User Interface
Das User Interface verfügt über verschiedene Reiter, welche auf der Linken Seite der Streamlit Seite ausgewählt werden können. Zu Beginn kommt man auf die Hauptseite unseres "RythmRadar", wo wir direkt die Hauptfunktion der App, die Musikerkennung in Anspruch nehmen können. Hier gibt es nun die Option, die Musikerkennung über das Mikrofon mit dem Knopf "Musik erkennen" zu starten. Ebenso gibt es die Möglichkeit eine Musikdatei mittels Drag-and-drop einzuspielen, oder diese mittels "Brows files" Knopf in den Dateien auszuwählen. Während man auf die Musikerkennung wartet werden von der App GIFs abgespielt, um die Wartezeit kürzer wirken zu lassen und das Interface aufzuwerten. Wenn ein Musikstück erkannt wird, werden Titel, Künstler sowie Album des entsprechenden Stücks wiedergegeben. Falls das Musikstück nicht erkannt wird, wird auf der Seite die Nachricht "Kein Erfolg. Bitte versuch es nochmal" dargestellt.

Wenn wir jetzt auf den Reiter links vom Hauptinterface gehen, kann man in verschiedene Reiter springen. Der zweite Reiter wurde mit "Meine erkannten Songs" benannt und gibt die Liste an Songs aus, welche der Benutzer der Oberfläche bereits erkennen lassen hat.

Als Letztes gibt es noch den Reiter "Bibliothek erweitern". Hier kann man, wie auch im Reiter "Musikerkennung" mittels Drag-and-drop oder mittels "Browse files" Musikstücke einspielen welche dann in die Datenbank mit aufgenommen werden. Für den Fall, dass ein Musikstück ohne hinterlegte Infos (Songname, Künstler, Album) in den Metadaten eingespielt wird, kann man diese Informationen händisch eintippen. Für den Fall, dass diese Informationen nicht vom Programm erkannt werden und diese auch nicht händisch eingetippt werden, wird der Song zwar in die Datenbank mit aufgenommen, jedoch wird dieser dann als "Unknown" gespeichert.

# Wie funktioniert das Programm ?

Wir haben Streamlit als Basis für unsere "App" und fürs Interface benutzt.

Anfangs werden Songs eingespielt und das Audio von jedem Song in kleine Zeitabschnitte gegliedert. Anschließend wird jeder kleine Teilabschnitt des Songs von der "time domain" mithilfe einer Fourier Transformation in die "frequency domain" umgewandelt um die enthaltenen Frequenzen zu analysieren. So wird ein Spektrogramm erstellt, welches die Amplituden der verschiedenen Frequenzen über die Zeit darstellt.

Anschließend werden die lautesten Frequenzen, sogenannte "Peaks", des Spektrogramms gefunden und zu "Fingerprints" zusammengeführt, welche charakteristisch für jeden Audioausschnitt sind. Diese "Peaks" sind meistens markante Töne.

Anschließend wird "Hashing" gemacht, was uns erlaubt, die Fingerprints in einem kompakteren Format zu speichern. Hier werden die Frequenzen und die Zeitunterschiede zwischen den Peaks in ein Format gespeichert, welches uns erlaubt, die eingespielten Songs mit jenen in der Datenbank abzugleichen.

Wenn es genügend Übereinstimmungen zwischen den gehashten Fingerprints von einem Song in der Datenbank mit jenen vom Song, welcher gerade eingespielt wurde gibt, gibt das Programm den Songtitel, den Künstler und das Album wieder, sofern diese hinterlegt sind.

# Erweiterungen
Erweiterungen welche implementiert wurden sind:
- Die Musikerkennung über das Mikrofon
- Bei erkennung eines Songs die Möglichkeit diesen direkt über Spotify oder YouTube abzuspielen, dabei wird direkt der Titel sowie der Künstler in die Suchleiste der jeweiligen Platform übergeben und dieser so direkt gesucht. 
- Es wurde ein Reiter "Erkannte Songs" erstellt welcher eine Liste der Songs wiedergibt, welche der Benutzer der Oberfläche bereits erkennen lassen hat.
- GIFs werden abgespielt, während man auf die Song-erkennung wartet.

# Quellen
Orientierung am vorherigen Projekt "Case Study"
https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf
https://www.cameronmacleod.com/blog/how-does-shazam-work
https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/
https://learningtofly.dev/blog/streamlit-class-based-app
https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf
https://photutils.readthedocs.io/en/stable/_modules/photutils/detection/core.html#find_peaks