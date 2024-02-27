# Abschlussprojekt_Musikerkennung

# Installation 
Damit das Programm funktioniert, müssen alle packages aus dem "requirements.txt" file installiert werden und die ".py" files ausgeführt werden. Anschließend kann die website mit dem Befehl "streamlit run user_interface.py", welcher in einen Terminal gschrieben werden muss, geöffnet werden. 


# Beschreibung der funktionalität des User interface



# Wie funktioniert das Programm ? 

Wir haben Streamlit als Basis für unser "App" und fürs Interface benutzt. 

Anfangs werden Songs eingespielt und das Audio vone jedem Song in kleine Zeitabschnitte gegliedert. Anschließend wird jeder kleine Teilabschnitt des Songs von der "time domain" mithilfe einer fourier Transformation in die "frequency domain" umgewandelt um die enthaltenen Frequenzen zu analysieren. So wird ein Spektogram erstellt, welches die Amplituden der verschiedenen Frequenzen über die Zeit darstellt.

Anschließend werden die lautesten frequenzen, sogenannte "Peaks", des Spektograms gefunden und zu "Fingerprints" zusammengeführt, welche charakteristisch für jeden Audioausschnitt sind. Diese "Peaks" sind meistens markante Töne.

Anschließend wird "Hashing" gemacht, was uns erlaubt die fingerprints in einem kompakteren Format zu speichern. Hier werden die Frequenzen und die Zeitunterschiede zwischen den Peaks in ein Format gespeichert, welches uns erlaubt, die eingespielten songs mit jenen in der Datenbank abzugleichen. 

Wenn es genügen Übereinstimmungen zwischen den gehashten fingerprints von einem Song in der Datenbank mit jenen vom Song, welcher gerade eingespielt wurde gibt, gibt das Programm den Songtitel, den Interpreter und das Album wieder.$$$$$$$$$$$$

# Quellen 
Orientierung am vorherigen Projekt "Case Study"
https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf
https://www.cameronmacleod.com/blog/how-does-shazam-work
https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/
https://learningtofly.dev/blog/streamlit-class-based-app