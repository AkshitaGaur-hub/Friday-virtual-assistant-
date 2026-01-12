# Raw file for debugging
import pyttsx3
import time

def speak(text):
    print("Speaking:", text)
    engine = pyttsx3.init('sapi5')   # 🔴 re-init every time
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

speak("Text to speech is working")
time.sleep(1)
speak("Second sentence test")
time.sleep(1)
speak("I am very happy to alive")
