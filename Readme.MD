# 🎙️ Real-Time Language Detection, Transcription & Subtitles

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Azure](https://img.shields.io/badge/Azure-Cognitive%20Services-0078D4)
![License](https://img.shields.io/badge/License-MIT-green)
![Teams](https://img.shields.io/badge/Microsoft-Teams-6264A7)

A powerful modular Python system that provides real-time language detection, speech transcription, and translation with live subtitles. Seamlessly integrates with Microsoft Teams for enhanced meeting accessibility and cross-language communication.

## 🌟 Features

- **Real-time language detection** - Automatically identifies the spoken language
- **Speech-to-text transcription** - Converts speech to text with high accuracy
- **Multi-language translation** - Translates content to your preferred language
- **Live subtitles** - Displays real-time subtitles over video content
- **Noise reduction** - Enhances audio quality for better transcription 
- **Microsoft Teams integration** - Works directly in Teams meetings
- **Modular architecture** - Easily extensible for custom requirements

## 📋 Requirements

- Python 3.7 or higher
- Azure subscription (free tier works for testing)
- Microsoft Teams (for Teams integration)
- Azure AD application (for Teams authentication)

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
   TEAMS_APP_ID=your_teams_app_id
   TEAMS_APP_PASSWORD=your_teams_app_password
   TEAMS_TENANT_ID=your_tenant_id
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

### Microsoft Teams Integration
```sh
python teams_app.py
```

## 🔌 Microsoft Teams Integration

1. **Register Azure AD application**
2. **Configure API permissions** (User.Read, OnlineMeetings.ReadWrite, etc.)
3. **Create client secret**
4. **Update `.env` file with Teams app details**

### Joining Teams Meetings
```python
from teams_integration import TeamsIntegration

teams = TeamsIntegration()
teams.initialize()
teams.join_meeting("https://teams.microsoft.com/l/meetup-join/your-meeting-link")
```

## 📦 Modules Overview

| Module | Description |
|--------|-------------|
| `audio_capture.py` | Captures audio from microphone or Teams meetings |
| `audio_preprocessing.py` | Processes audio to reduce noise and improve quality |
| `language_detection.py` | Identifies the language being spoken |
| `speech_to_text.py` | Transcribes speech to text using Azure Speech Services |
| `translation.py` | Translates text between languages using Azure Translator |
| `subtitle_renderer.py` | Displays subtitles on screen |
| `realtime_subtitle_system.py` | Coordinates all modules and manages the workflow |

## 🔧 Advanced Configuration

### Custom Language Settings
Edit `config.py`:
```python
DEFAULT_SOURCE_LANGUAGE = "auto"
DEFAULT_TARGET_LANGUAGE = "en"
LANGUAGE_PRIORITY = ["en", "es", "fr", "de", "ja", "zh"]
CONFIDENCE_THRESHOLD = 0.7
```

### Performance Tuning
In `modules/audio_preprocessing.py`
```python
CHUNK_SIZE = 2048
NOISE_SUPPRESSION = 0.2
```

In `modules/realtime_subtitle_system.py`
```python
TRANSLATION_BATCH_SIZE = 5
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No audio input | Check microphone permissions and PyAudio installation |
| Authentication errors | Verify Azure keys and AD application configuration |
| Teams meeting access denied | Ensure proper API permissions and admin consent |
| High latency | Adjust chunk size and batch processing settings |
| Language detection issues | Increase the minimum text length for detection |

Enable detailed logging:
```sh
DEBUG_LEVEL=DEBUG
```

## 🌐 Supported Languages

Supports 70+ languages including English, Spanish, French, German, Chinese, Japanese, Russian, Arabic, Hindi, and more.

```python
from teams_integration import TeamsIntegration

teams = TeamsIntegration()
languages = teams.get_supported_languages()
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgements

- [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)
- [Microsoft Graph API](https://developer.microsoft.com/en-us/graph)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [RNNoise](https://github.com/xiph/rnnoise)

---

<p align="center">
  Made with ❤️ for better communication across languages
</p>
