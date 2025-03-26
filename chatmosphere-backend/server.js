require('dotenv').config();
const cors = require('cors');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const sdk = require('microsoft-cognitiveservices-speech-sdk');
const axios = require('axios');
const { TextAnalyticsClient, AzureKeyCredential } = require('@azure/ai-text-analytics');
const fs = require('fs');

const app = express();
app.use(cors({
  origin: "http://127.0.0.1:8080",
  methods: ["GET", "POST"]
}));

const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://127.0.0.1:8080",
    methods: ["GET", "POST"]
  },
  transports: ["websocket", "polling"]
});

const PORT = process.env.PORT || 3001;

// Validate environment variables
const requiredEnvVars = ['SPEECH_KEY', 'SPEECH_REGION', 'TRANSLATOR_KEY', 'TEXT_ANALYTICS_KEY'];
requiredEnvVars.forEach(varName => {
  if (!process.env[varName]) throw new Error(`Missing ${varName} in .env`);
});

// Azure configurations
const speechConfig = sdk.SpeechConfig.fromSubscription(
  process.env.SPEECH_KEY,
  process.env.SPEECH_REGION
);

const textAnalyticsClient = new TextAnalyticsClient(
  process.env.TEXT_ANALYTICS_ENDPOINT,
  new AzureKeyCredential(process.env.TEXT_ANALYTICS_KEY)
);

// Audio validation (0.5 seconds minimum)
function validateAudioFormat(audioBuffer) {
  const BYTES_PER_SECOND = 16000 * 2; // 16kHz * 16-bit
  const minBytes = BYTES_PER_SECOND * 0.5;
  if (audioBuffer.length < minBytes) {
    throw new Error(`Audio chunk too short: ${audioBuffer.length} bytes (needs ≥${minBytes} bytes)`);
  }
}

async function speechToText(audioBuffer) {
  validateAudioFormat(audioBuffer);
  return new Promise((resolve, reject) => {
    const pushStream = sdk.AudioInputStream.createPushStream();
    pushStream.write(audioBuffer);
    pushStream.close();

    const audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);
    const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

    recognizer.recognizeOnceAsync(
      result => {
        recognizer.close();
        result.reason === sdk.ResultReason.RecognizedSpeech 
          ? resolve(result.text)
          : reject(new Error(result.errorDetails));
      },
      error => {
        recognizer.close();
        reject(error);
      }
    );
  });
}

async function detectLanguage(text) {
  const [result] = await textAnalyticsClient.detectLanguage([text]);
  return result.primaryLanguage.iso6391Name || 'en';
}

async function translateText(text, targetLang = 'es') {
  const response = await axios.post(
    `${process.env.TRANSLATOR_ENDPOINT || 'https://api.cognitive.microsofttranslator.com'}/translate?api-version=3.0&to=${targetLang}`,
    [{ Text: text }],
    {
      headers: {
        'Ocp-Apim-Subscription-Key': process.env.TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': process.env.TRANSLATOR_REGION,
        'Content-Type': 'application/json'
      }
    }
  );
  return response.data[0].translations[0].text;
}

io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);
  let processingQueue = [];
  let isProcessing = false;

  const processQueue = async () => {
    if (isProcessing || !processingQueue.length) return;
    isProcessing = true;
    
    try {
      const audioData = processingQueue.shift();
      console.log(`Processing ${audioData.length} byte chunk`);
      
      const transcription = await speechToText(audioData);
      const sourceLang = await detectLanguage(transcription);
      const translation = await translateText(transcription);
      
      socket.emit('translation_result', {
        original: transcription,
        translated: translation,
        detectedLanguage: sourceLang
      });
    } catch (error) {
      console.error('Processing error:', error.message);
      socket.emit('processing_error', error.message);
    } finally {
      isProcessing = false;
      processQueue();
    }
  };

  socket.on('audio_chunk', (data) => {
    processingQueue.push(Buffer.from(data));
    processQueue();
  });

  socket.on('disconnect', () => {
    console.log(`Client disconnected: ${socket.id}`);
    processingQueue = [];
  });
});

app.get('/test-speech', async (req, res) => {
  try {
    const audioBuffer = fs.readFileSync('test_audio.wav');
    const text = await speechToText(audioBuffer);
    res.json({ transcription: text });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

server.listen(PORT, () => console.log(`Server running on port ${PORT}`));