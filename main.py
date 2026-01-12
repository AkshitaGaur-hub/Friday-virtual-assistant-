import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import requests
import musicLibrary
import threading

assistant_busy = False

# ===================== CONFIG =====================
API_KEY = "efee005b78c544de80ac0aa025c5bf5a"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
recognizer.energy_threshold = 300


# ===================== TTS (FIXED) =====================
def speak(text):
    print("Friday:", text)
    engine = pyttsx3.init('sapi5')   # 🔥 re-init every time
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.2)
# ====================AI AUTOMATION =========================
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"You are Friday, a concise voice assistant. Answer briefly.\nUser: {prompt}\nFriday:",
                "stream": False,
                "options": {
                    "temperature": 0.4,
                    "num_predict": 80   # 🔥 LIMIT TOKENS (VERY IMPORTANT)
                }
            },
            timeout=180   # 🔥 first-time models need more time
        )

        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return "I am having trouble thinking right now."

    except Exception as e:
        print("Ollama Error:", e)
        return "Ollama is not responding. Please wait a moment."

# ===================== AI THREAD ==========================
def handle_ai(command):
    global assistant_busy
    assistant_busy = True

    answer = ask_ollama(command)
    speak(answer)

    assistant_busy = False


# ===================== COMMAND HANDLER =====================
def processCommand(command):
    command = command.lower().strip()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif "open chat gpt" in command or "open chatgpt" in command:
        speak("Opening Chat GPT")
        webbrowser.open("https://chat.openai.com")

    elif command.startswith("play"):
        try:
            song = command.split(" ", 1)[1]
            link = musicLibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        except:
            speak("Song not found in your library")

    elif "news" in command:
        fetch_news()

    # else:
    #     speak("Let me think.")
    #     answer = ask_ollama(command)
    #     speak(answer)
    #     time.sleep(1.2)   

    else:
        speak("Thinking.")
        handle_ai(command)        

# ===================== NEWS =====================
def fetch_news():
    try:
        r = requests.get(NEWS_URL, timeout=5)

        if r.status_code != 200:
            speak("Unable to fetch news")
            return

        data = r.json()
        articles = data.get("articles", [])

        if not articles:
            speak("No news available right now")
            return

        speak("Here are the top headlines")

        for article in articles[:5]:
            title = article.get("title")
            if title:
                speak(title)
                time.sleep(0.3)

    except Exception as e:
        print("News Error:", e)
        speak("There was an error fetching the news")

# ===================== MAIN =====================
if __name__ == "__main__":
    speak("Initializing Friday. How can I help you?")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                if assistant_busy:
                    time.sleep(0.1)
                    continue
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                try:
                    word = recognizer.recognize_google(audio, language="en-IN")
                except sr.RequestError:
                    print("Google Speech API unavailable")
                    continue

                print("Heard:", word)

                if "friday" in word.lower():
                    speak("Yes?")
                    time.sleep(0.5)

                    print("Listening for command...")
                    audio_cmd = recognizer.listen(source, timeout=10, phrase_time_limit=6)
                    command = recognizer.recognize_google(audio_cmd, language="en-IN")
                    print("Command:", command)

                    processCommand(command)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except KeyboardInterrupt:
                speak("Shutting down")
                break
# pygame is library for mp3 file 