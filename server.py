import os
import time
from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import socketio
import asyncio

load_dotenv()

app = FastAPI()

# Configure Socket.IO
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)
asgi_app = socketio.ASGIApp(sio, app)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Azure Configuration
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"

class AzureToken:
    def __init__(self):
        self.token = None
        self.expires_at = 0

    async def refresh(self):
        try:
            response = requests.post(
                f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issuetoken",
                headers={"Ocp-Apim-Subscription-Key": SPEECH_KEY},
                timeout=5
            )
            response.raise_for_status()
            self.token = response.text
            self.expires_at = time.time() + 540  # 9 minutes
            return True
        except Exception as e:
            print(f"Token refresh failed: {str(e)}")
            return False

azure_token = AzureToken()

def validate_audio_format(audio_data: bytes):
    required_bytes = 16000 * 2 * 0.5  # 0.5 seconds of 16kHz 16-bit audio
    if len(audio_data) < required_bytes:
        raise ValueError(f"Audio too short: {len(audio_data)} bytes, need {required_bytes}")

async def translate_text(text: str, target_language: str = 'hi') -> str:
    """Translate text using Microsoft Translator API"""
    if not text or not TRANSLATOR_KEY:
        return text
    
    try:
        headers = {
            'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
            'Ocp-Apim-Subscription-Region': SPEECH_REGION,
            'Content-type': 'application/json'
        }
        
        params = {
            'api-version': '3.0',
            'to': target_language
        }
        
        body = [{'text': text}]
        
        response = requests.post(
            f"{TRANSLATOR_ENDPOINT}/translate",
            headers=headers,
            params=params,
            json=body
        )
        response.raise_for_status()
        
        translation = response.json()[0]['translations'][0]['text']
        return translation
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original if translation fails

async def speech_to_text(audio_data: bytes):
    validate_audio_format(audio_data)
    
    if time.time() >= azure_token.expires_at or not azure_token.token:
        if not await azure_token.refresh():
            raise Exception("Azure token refresh failed")

    endpoint = f"https://{SPEECH_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US"
    headers = {
        "Authorization": f"Bearer {azure_token.token}",
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json"
    }

    try:
        response = requests.post(endpoint, headers=headers, data=audio_data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["DisplayText"] if result["RecognitionStatus"] == "Success" else ""
    except Exception as e:
        print(f"Speech recognition error: {str(e)}")
        return ""

@sio.event
async def connect(sid, environ, auth):
    try:
        print(f"Client connected: {sid}, Auth: {auth}")
        await sio.emit("connection_success", {"sid": sid}, room=sid)
        await azure_token.refresh()
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("audio_chunk")
async def process_audio(sid, audio_data):
    try:
        if not isinstance(audio_data, bytes):
            raise ValueError("Audio data must be in bytes format")
            
        english_text = await speech_to_text(audio_data)
        if english_text:
            hindi_translation = await translate_text(english_text, 'hi')
            
            await sio.emit("translation_result", {
                "original": english_text,
                "translated": hindi_translation,
                "detectedLanguage": "en"
            }, room=sid)
    except Exception as e:
        print(f"Processing error for {sid}: {str(e)}")
        await sio.emit("processing_error", {
            "error": str(e),
            "sid": sid
        }, room=sid)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:asgi_app",
        host="0.0.0.0",
        port=3001,
        reload=True,
        ws="websockets"
    )