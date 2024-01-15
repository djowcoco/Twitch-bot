import time
import keyboard
import whisper
import sounddevice as sd
import numpy as np
from obswebsocket import obsws, requests
import logging
logging.basicConfig(level=logging.DEBUG)

model = whisper.load_model("base")

def transcribe_audio():
    sd.default.device = 1
    duration = 3  # Durée réduite à 3 secondes
    samplerate = 18000

    print("Enregistrement en cours...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    print("Enregistrement terminé.")

    audio = np.array(recording).astype(np.float32).flatten()
    print("Taille de l'audio:", audio.size)

    result = model.transcribe(audio, language="fr")
    print("Texte transcrit en français : ", result["text"])
    return result["text"]

def connectobs():
    host = "localhost"
    port = 4455  # Remplacez par le port de votre serveur WebSocket OBS
    password = "f08H00EOsj0FmOpP"  # Si vous avez configuré un mot de passe

    ws = obsws(host, port, password)
    ws.connect()

    print("Connecté à OBS")

    return ws
def show__or_hide_source(ws,source_name,enabled):
    sceneName = ws.call(requests.GetCurrentProgramScene()).getCurrentProgramSceneName()
    result = ws.call(requests.GetSceneItemId(sceneName=sceneName,sourceName=source_name))
    sceneItemId = result.getSceneItemId()
    ws.call(requests.SetSceneItemEnabled(sceneName=sceneName, sceneItemId=sceneItemId, sceneItemEnabled=enabled))

def show_source(ws,source_name):
    show__or_hide_source(ws,source_name,True)

def hide_source(ws,source_name):
    show__or_hide_source(ws,source_name,False)

if __name__ == "__main__":
    ws = connectobs()
    
    try:
        while True:  # Boucle infinie
            transcribed_text = transcribe_audio().lower()
            print(transcribed_text)

            if "chien" in transcribed_text:
                show_source(ws, "rey.png")
            elif "panier" in transcribed_text:
                hide_source(ws, "rey.png")

            time.sleep(2)  # Pause de 2 secondes

    except KeyboardInterrupt:
        print("Arrêt du script par l'utilisateur")
        ws.disconnect()

#bosser sur la biblio pokemon