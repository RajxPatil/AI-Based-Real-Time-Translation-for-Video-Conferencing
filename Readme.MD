<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-Time Language Detection, Transcription & Subtitles</title>
    <style>
        :root {
            --primary-color: #4285F4;
            --secondary-color: #34A853;
            --accent-color: #FBBC05;
            --text-color: #333;
            --light-bg: #f8f9fa;
            --code-bg: #272822;
            --code-color: #f8f8f2;
            --border-color: #ddd;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1, h2, h3, h4 {
            font-weight: 600;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: var(--primary-color);
        }
        
        h1 {
            font-size: 2.5em;
            text-align: center;
            margin-top: 0.5em;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 10px;
        }
        
        h2 {
            font-size: 1.8em;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 5px;
        }
        
        h2 .emoji {
            margin-right: 10px;
        }
        
        h3 {
            font-size: 1.3em;
        }
        
        a {
            color: var(--primary-color);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        code {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: var(--light-bg);
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        pre {
            background-color: var(--code-bg);
            color: var(--code-color);
            padding: 16px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }
        
        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            border-radius: 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);
        }
        
        table th {
            background-color: var(--primary-color);
            color: white;
            padding: 12px 15px;
            text-align: left;
        }
        
        table td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
        }
        
        table tr:nth-child(even) {
            background-color: var(--light-bg);
        }
        
        ul, ol {
            padding-left: 30px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        .version-badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            background-color: var(--light-bg);
            font-size: 0.9em;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>Real-Time Language Detection, Transcription & Subtitles</h1>
    
    <div class="version-badges">
        <span class="badge">Version 1.0.0</span>
        <span class="badge">Python 3.7+</span>
        <span class="badge">MIT License</span>
    </div>
    
    <p>A powerful modular Python system that provides real-time language detection, speech transcription, and translation with live subtitles. Seamlessly integrates with Microsoft Teams for enhanced meeting accessibility and cross-language communication.</p>
    
    <h2><span class="emoji">🌟</span> Features</h2>
    <ul>
        <li><strong>Real-time language detection</strong> - Automatically identifies the spoken language</li>
        <li><strong>Speech-to-text transcription</strong> - Converts speech to text with high accuracy</li>
        <li><strong>Multi-language translation</strong> - Translates content to your preferred language</li>
        <li><strong>Live subtitles</strong> - Displays real-time subtitles over video content</li>
        <li><strong>Noise reduction</strong> - Enhances audio quality for better transcription</li>
        <li><strong>Microsoft Teams integration</strong> - Works directly in Teams meetings</li>
        <li><strong>Modular architecture</strong> - Easily extensible for custom requirements</li>
    </ul>
    
    <h2><span class="emoji">📋</span> Requirements</h2>
    <ul>
        <li>Python 3.7 or higher</li>
        <li>Azure subscription (free tier works for testing)</li>
        <li>Microsoft Teams (for Teams integration)</li>
        <li>Azure AD application (for Teams authentication)</li>
    </ul>
    
    <h2><span class="emoji">🔧</span> Installation</h2>
    
    <h3>1. Clone the repository</h3>
    <pre><code>git clone https://github.com/yourusername/real-time-subtitles.git
cd real-time-subtitles</code></pre>
    
    <h3>2. Set up a virtual environment</h3>
    <pre><code># Create environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Activate environment (macOS/Linux)
source venv/bin/activate</code></pre>
    
    <h3>3. Install dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>
    
    <p>Note: For PyAudio installation issues:</p>
    <ul>
        <li>Windows: <code>pip install pipwin</code> then <code>pipwin install pyaudio</code></li>
        <li>macOS: <code>brew install portaudio</code> then <code>pip install pyaudio</code></li>
        <li>Linux: <code>sudo apt-get install python3-pyaudio</code></li>
    </ul>
    
    <h3>4. Create Azure resources</h3>
    <p>You'll need the following Azure services:</p>
    <ul>
        <li><strong>Speech Service</strong> - For speech recognition and transcription</li>
        <li><strong>Translator</strong> - For language translation</li>
        <li><strong>Language Service</strong> - For language detection</li>
    </ul>
    <p>Follow Azure's <a href="https://docs.microsoft.com/en-us/azure/cognitive-services/">documentation</a> to create these resources and obtain API keys.</p>
    
    <h3>5. Configure environment variables</h3>
    <p>Create a <code>.env</code> file in the project root directory:</p>
    <pre><code># Azure Services
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_speech_region
AZURE_TRANSLATOR_KEY=your_translator_key
AZURE_TRANSLATOR_REGION=your_translator_region
AZURE_LANGUAGE_KEY=your_language_key
AZURE_LANGUAGE_ENDPOINT=https://your-language-resource.cognitiveservices.azure.com

# Teams Integration (if using)
TEAMS_APP_ID=your_teams_app_id
TEAMS_APP_PASSWORD=your_teams_app_password
TEAMS_TENANT_ID=your_tenant_id</code></pre>
    
    <h2><span class="emoji">🚀</span> Usage</h2>
    
    <h3>Standalone Application</h3>
    <p>Run the standalone application with GUI:</p>
    <pre><code>python app.py</code></pre>
    <p>This will launch a user interface where you can:</p>
    <ul>
        <li>Start/stop the subtitle system</li>
        <li>Change the target language</li>
        <li>View real-time transcription and translation</li>
    </ul>
    
    <h3>Command Line Interface</h3>
    <p>For headless or server environments:</p>
    <pre><code>python main.py --target-language en --source-language auto</code></pre>
    
    <h3>Microsoft Teams Integration</h3>
    <p>Run the Teams-specific application:</p>
    <pre><code>python teams_app.py</code></pre>
    <p>This interface allows you to:</p>
    <ul>
        <li>Enter Teams meeting links to join</li>
        <li>Control subtitle settings during meetings</li>
        <li>Provide real-time translation to meeting participants</li>
    </ul>
    
    <h2><span class="emoji">🔌</span> Microsoft Teams Integration</h2>
    
    <h3>Setting Up Teams Integration</h3>
    <ol>
        <li>
            <strong>Register an Azure AD application</strong>:
            <ul>
                <li>Go to <a href="https://portal.azure.com">Azure Portal</a> → Azure Active Directory → App registrations</li>
                <li>Create a new registration for your application</li>
                <li>Set up proper redirect URIs (e.g., <code>http://localhost:8000/auth/callback</code>)</li>
                <li>Note down the Application (client) ID and Directory (tenant) ID</li>
            </ul>
        </li>
        <li>
            <strong>Configure API permissions</strong>:
            <ul>
                <li>Microsoft Graph API permissions:
                    <ul>
                        <li><code>User.Read</code></li>
                        <li><code>OnlineMeetings.ReadWrite</code></li>
                        <li><code>Calls.JoinGroupCall.All</code></li>
                        <li><code>Calls.AccessMedia.All</code></li>
                    </ul>
                </li>
                <li>Grant admin consent</li>
            </ul>
        </li>
        <li>
            <strong>Create a client secret</strong>:
            <ul>
                <li>Under "Certificates & secrets", create a new client secret</li>
                <li>Save the value immediately (you won't be able to see it again)</li>
            </ul>
        </li>
        <li><strong>Update your environment variables</strong> with the Teams app details</li>
    </ol>
    
    <h3>Joining Teams Meetings</h3>
    <p>The application can join Teams meetings in two ways:</p>
    <ol>
        <li>
            <strong>Through the user interface</strong>:
            <ul>
                <li>Enter the meeting link in the UI</li>
                <li>Click "Join Meeting"</li>
            </ul>
        </li>
        <li>
            <strong>Programmatically</strong>:
            <pre><code>from teams_integration import TeamsIntegration
   
teams = TeamsIntegration()
teams.initialize()
teams.join_meeting("https://teams.microsoft.com/l/meetup-join/your-meeting-link")</code></pre>
        </li>
    </ol>
    
    <h2><span class="emoji">📦</span> Modules Overview</h2>
    <p>The system is built with a modular architecture for flexibility and extensibility:</p>
    
    <table>
        <thead>
            <tr>
                <th>Module</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>audio_capture.py</code></td>
                <td>Captures audio from microphone or Teams meetings</td>
            </tr>
            <tr>
                <td><code>audio_preprocessing.py</code></td>
                <td>Processes audio to reduce noise and improve quality</td>
            </tr>
            <tr>
                <td><code>language_detection.py</code></td>
                <td>Identifies the language being spoken</td>
            </tr>
            <tr>
                <td><code>speech_to_text.py</code></td>
                <td>Transcribes speech to text using Azure Speech Services</td>
            </tr>
            <tr>
                <td><code>translation.py</code></td>
                <td>Translates text between languages using Azure Translator</td>
            </tr>
            <tr>
                <td><code>subtitle_renderer.py</code></td>
                <td>Displays subtitles on screen</td>
            </tr>
            <tr>
                <td><code>realtime_subtitle_system.py</code></td>
                <td>Coordinates all modules and manages the workflow</td>
            </tr>
        </tbody>
    </table>
    
    <h2><span class="emoji">🔧</span> Advanced Configuration</h2>
    
    <h3>Custom Language Settings</h3>
    <p>Edit <code>config.py</code> to modify language settings:</p>
    <pre><code>DEFAULT_SOURCE_LANGUAGE = "auto"  # "auto" for automatic detection
DEFAULT_TARGET_LANGUAGE = "en"    # Default target language

# Languages priority for detection
LANGUAGE_PRIORITY = ["en", "es", "fr", "de", "ja", "zh"]

# Recognition confidence threshold 
CONFIDENCE_THRESHOLD = 0.7</code></pre>
    
    <h3>Performance Tuning</h3>
    <p>For better performance on lower-powered devices:</p>
    <pre><code># In modules/audio_preprocessing.py
CHUNK_SIZE = 2048       # Increase for better performance, decrease for lower latency
NOISE_SUPPRESSION = 0.2 # Adjust between 0.0 (none) and 1.0 (aggressive)

# In modules/realtime_subtitle_system.py
TRANSLATION_BATCH_SIZE = 5  # Increase to reduce API calls</code></pre>
    
    <h2><span class="emoji">🐛</span> Troubleshooting</h2>
    
    <h3>Common Issues</h3>
    <table>
        <thead>
            <tr>
                <th>Issue</th>
                <th>Solution</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>No audio input detected</td>
                <td>Check microphone permissions and PyAudio installation</td>
            </tr>
            <tr>
                <td>Authentication errors</td>
                <td>Verify Azure keys and AD application configuration</td>
            </tr>
            <tr>
                <td>Teams meeting access denied</td>
                <td>Ensure proper API permissions and admin consent</td>
            </tr>
            <tr>
                <td>High latency</td>
                <td>Adjust chunk size and batch processing settings</td>
            </tr>
            <tr>
                <td>Language detection issues</td>
                <td>Increase the minimum text length for detection</td>
            </tr>
        </tbody>
    </table>
    
    <h3>Logs</h3>
    <p>Enable detailed logging by setting the environment variable:</p>
    <pre><code>DEBUG_LEVEL=DEBUG</code></pre>
    <p>Logs are stored in the <code>logs</code> directory by default.</p>
    
    <h2><span class="emoji">🌐</span> Supported Languages</h2>
    <p>The system supports 70+ languages for transcription and translation, including:</p>
    <ul>
        <li>English (en)</li>
        <li>Spanish (es)</li>
        <li>French (fr)</li>
        <li>German (de)</li>
        <li>Chinese (zh-Hans, zh-Hant)</li>
        <li>Japanese (ja)</li>
        <li>Russian (ru)</li>
        <li>Arabic (ar)</li>
        <li>Hindi (hi)</li>
        <li><em>And many more</em></li>
    </ul>
    
    <p>Full language list is available through the API:</p>
    <pre><code>from teams_integration import TeamsIntegration

teams = TeamsIntegration()
languages = teams.get_supported_languages()</code></pre>
    
    <h2><span class="emoji">🤝</span> Contributing</h2>
    <p>Contributions are welcome! Please feel free to submit a Pull Request.</p>
    <ol>
        <li>Fork the repository</li>
        <li>Create your feature branch (<code>git checkout -b feature/amazing-feature</code>)</li>
        <li>Commit your changes (<code>git commit -m 'Add some amazing feature'</code>)</li>
        <li>Push to the branch (<code>git push origin feature/amazing-feature</code>)</li>
        <li>Open a Pull Request</li>
    </ol>
    
    <h2><span class="emoji">📄</span> License</h2>
    <p>This project is licensed under the MIT License - see the LICENSE file for details.</p>
    
    <h2><span class="emoji">🙏</span> Acknowledgements</h2>
    <ul>
        <li><a href="https://azure.microsoft.com/en-us/services/cognitive-services/">Azure Cognitive Services</a> for speech and language APIs</li>
        <li><a href="https://developer.microsoft.com/en-us/graph">Microsoft Graph API</a> for Teams integration</li>
        <li><a href="https://people.csail.mit.edu/hubert/pyaudio/">PyAudio</a> for audio processing capabilities</li>
        <li><a href="https://github.com/xiph/rnnoise">RNNoise</a> for noise suppression algorithms</li>
    </ul>
    
    <div class="footer">
        <p>Made with ❤️ for better communication across languages</p>
    </div>
</body>
</html>
