"""
Diagnostic: verify voice transcription (OpenAI and/or free Google path).
Run from project root: python check_voice_api.py
"""
import os
import sys
import tempfile
import wave
from pathlib import Path

# Load .env same way as gradio_app
root = Path(__file__).resolve().parent
for name in (".env", "phase_iii/.env"):
    p = root / name.replace("/", os.sep)
    if p.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(p, override=True)
            print(f"Loaded: {p}")
        except ImportError:
            print("Install python-dotenv: pip install python-dotenv")
            sys.exit(1)

key = (os.getenv("OPENAI_API_KEY") or "").strip().strip('"\'')
print(f"OPENAI_API_KEY set: {bool(key)}")
if key and not key.startswith("sk-placeholder"):
    print(f"Key prefix: {key[:15]}...{key[-4:]}")

# Minimal 0.5s WAV (silence) for test
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    wav_path = tmp.name
try:
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 8000)
except Exception as e:
    print(f"Could not create test WAV: {e}")
    sys.exit(1)

def cleanup():
    try:
        os.unlink(wav_path)
    except Exception:
        pass

# 1. Try OpenAI if key available
if key and not key.startswith("sk-placeholder"):
    print("Testing OpenAI Whisper API...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        with open(wav_path, "rb") as f:
            r = client.audio.transcriptions.create(model="whisper-1", file=f, language="en")
        print("OpenAI Whisper OK. Transcript:", repr(r.text))
        cleanup()
        print("Voice API check passed.")
        sys.exit(0)
    except Exception as e:
        err = str(e)
        print(f"OpenAI error: {type(e).__name__}: {e}")
        if "429" in err or "quota" in err.lower():
            print("--> Quota/billing issue. Using free path (Google) instead.")

# 2. Try free path: SpeechRecognition + Google
print("Testing free path (SpeechRecognition + Google)...")
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source, duration=5)
    t = r.recognize_google(audio, language="en-US")
    print("Google Speech OK. Transcript:", repr(t))
except ImportError:
    print("Install free voice: pip install SpeechRecognition")
    cleanup()
    sys.exit(1)
except sr.UnknownValueError:
    print("Google Speech OK (no speech in test audio, but API works).")
except sr.RequestError as e:
    print(f"Google Speech error: {e}")
    cleanup()
    sys.exit(1)
except Exception as e:
    print(f"Google Speech error: {type(e).__name__}: {e}")
    cleanup()
    sys.exit(1)

cleanup()
print("Voice API check passed (free path).")
