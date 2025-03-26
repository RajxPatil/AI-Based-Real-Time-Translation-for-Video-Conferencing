# 🎧 Real-Time Language Detection, Transcription & Subtitles

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Azure](https://img.shields.io/badge/Azure-Cognitive%20Services-0078D4)
![License](https://img.shields.io/badge/License-MIT-green)
![Jitsi](https://img.shields.io/badge/Jitsi-Video%20Calling-0098D4)

A powerful modular Python system that provides real-time language detection, speech transcription, and translation with live subtitles. Seamlessly integrates with Jitsi for video calling and Microsoft Teams for enhanced meeting accessibility and cross-language communication.

## 🌟 Features

- **Real-time language detection** - Automatically identifies the spoken language using Azure Cognitive Services
- **Speech-to-text transcription** - Converts speech to text with high accuracy
- **Multi-language translation** - Translates content to your preferred language
- **Live subtitles** - Displays real-time subtitles over video content
- **Noise reduction** - Enhances audio quality for better transcription 
- **Jitsi video calling integration** - Works directly in Jitsi meetings
- **WebSockets for fast data passage** - Ensures low-latency communication for real-time updates
- **Modular architecture** - Easily extensible for custom requirements

## 👌 Requirements

- Python 3.7 or higher
- Azure subscription (free tier works for testing)
- Jitsi Meet (for video calling integration)
- WebSockets library (for fast data passage)
- Azure AD application (for authentication)

## 🔧 Installation

1. **Clone the repository**
```sh
git clone https://github.com/yourusername/real-time-subtitles.git
cd real-time-subtitles
```

2. **Set up a virtual environment**
```sh
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. **Install dependencies**
```sh
pip install -r requirements.txt
```

4. **Configure Azure services**
   - Create Speech Service, Translator, and Language Service resources in Azure
   - Note down the API keys and endpoints

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```sh
   AZURE_SPEECH_KEY=your_speech_key
   AZURE_SPEECH_REGION=your_speech_region
   AZURE_TRANSLATOR_KEY=your_translator_key
   AZURE_TRANSLATOR_REGION=your_translator_region
   AZURE_LANGUAGE_KEY=your_language_key
   AZURE_LANGUAGE_ENDPOINT=https://your-language-resource.cognitiveservices.azure.com
   JITSI_SERVER_URL=https://meet.jit.si
   ```

## 🚀 Usage

### Standalone Application
```sh
python app.py
```

### Command Line Interface
```sh
python main.py --target-language en --source-language auto
```

### Jitsi Video Calling Integration
```sh
python jitsi_app.py
```

## 🔌 Jitsi Integration

1. **Register Jitsi API credentials**
2. **Update `.env` file with Jitsi server details**
3. **Run the integration module**

### Joining Jitsi Meetings
```python
from jitsi_integration import JitsiIntegration

jitsi = JitsiIntegration()
jitsi.initialize()
jitsi.join_meeting("https://meet.jit.si/your-meeting-link")
```

## 🛀 WebSockets for Real-Time Updates

We use WebSockets to ensure fast data passage and low-latency communication for real-time subtitles and translations.

### WebSocket Server Example
```python
import websockets
import asyncio

async def handler(websocket, path):
    async for message in websocket:
        await websocket.send(f"Received: {message}")

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

## 🌟 Advanced Configuration

### Custom Language Settings
Edit `config.py`:
```python
DEFAULT_SOURCE_LANGUAGE = "auto"
DEFAULT_TARGET_LANGUAGE = "en"
LANGUAGE_PRIORITY = ["en", "es", "fr", "de", "ja", "zh"]
CONFIDENCE_THRESHOLD = 0.7
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No audio input | Check microphone permissions and PyAudio installation |
| Authentication errors | Verify Azure keys and Jitsi server configuration |
| Jitsi meeting access denied | Ensure proper API permissions and authentication |
| High latency | Optimize WebSockets settings and chunk processing |

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgements

- [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)
- [Jitsi Meet](https://meet.jit.si)
- [WebSockets](https://websockets.readthedocs.io)

---

<p align="center">
  Made with ❤️ for better communication across languages
</p>
