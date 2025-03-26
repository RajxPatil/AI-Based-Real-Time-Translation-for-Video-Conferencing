const JitsiMeetExternalAPI = window.JitsiMeetExternalAPI;
const socket = io('http://localhost:3001', {
  transports: ["websocket", "polling"]
});

// Audio configuration
const AUDIO_CONFIG = {
  TARGET_SAMPLE_RATE: 16000,
  BUFFER_DURATION: 0.6, // 600ms buffers
  CHANNELS: 1
};

let audioContext, processor, mediaStream;
const subtitleElement = document.getElementById('subtitle-overlay');

// Initialize Jitsi with audio constraints
const api = new JitsiMeetExternalAPI('meet.jit.si', {
  roomName: 'LiveSubtitleRoom',
  parentNode: document.querySelector('#jitsi-container'),
  configOverwrite: {
    constraints: {
      audio: {
        sampleRate: AUDIO_CONFIG.TARGET_SAMPLE_RATE,
        channelCount: AUDIO_CONFIG.CHANNELS
      }
    }
  }
});

function initializeAudioProcessing() {
  navigator.mediaDevices.getUserMedia({
    audio: {
      sampleRate: AUDIO_CONFIG.TARGET_SAMPLE_RATE,
      channelCount: AUDIO_CONFIG.CHANNELS,
      sampleSize: 16,
      echoCancellation: false,
      autoGainControl: false
    }
  }).then(stream => {
    mediaStream = stream;
    audioContext = new AudioContext({ sampleRate: AUDIO_CONFIG.TARGET_SAMPLE_RATE });
    
    const source = audioContext.createMediaStreamSource(stream);
    const bufferSize = Math.floor(AUDIO_CONFIG.TARGET_SAMPLE_RATE * AUDIO_CONFIG.BUFFER_DURATION);
    
    processor = audioContext.createScriptProcessor(bufferSize, 1, 1);
    let bufferAccumulator = new Float32Array(0);

    processor.onaudioprocess = (e) => {
      const inputBuffer = e.inputBuffer.getChannelData(0);
      bufferAccumulator = concatenateBuffers(bufferAccumulator, inputBuffer);
      
      if (bufferAccumulator.length >= bufferSize) {
        const sendBuffer = bufferAccumulator.slice(0, bufferSize);
        socket.emit('audio_chunk', convertFloat32ToInt16(sendBuffer));
        bufferAccumulator = bufferAccumulator.slice(bufferSize);
      }
    };

    source.connect(processor);
    processor.connect(audioContext.destination);
  }).catch(console.error);
}

function concatenateBuffers(a, b) {
  const result = new Float32Array(a.length + b.length);
  result.set(a);
  result.set(b, a.length);
  return result;
}

function convertFloat32ToInt16(buffer) {
  const int16Buffer = new Int16Array(buffer.length);
  for (let i = 0; i < buffer.length; i++) {
    int16Buffer[i] = Math.min(1, Math.max(-1, buffer[i])) * 32767;
  }
  return int16Buffer;
}

// Jitsi event handlers
api.on('ready', () => !api.isAudioMuted() && initializeAudioProcessing());
api.addListener('audioMuteStatusChanged', ({ muted }) => {
  if (muted) {
    mediaStream?.getTracks().forEach(t => t.stop());
    processor?.disconnect();
    audioContext?.close();
  } else {
    initializeAudioProcessing();
  }
});

// Socket.IO handlers
socket.on('translation_result', ({ original, translated }) => {
  subtitleElement.innerHTML = `
    <div class="original">${original}</div>
    <div class="translated">${translated}</div>
  `;
  clearTimeout(subtitleElement.timeout);
  subtitleElement.timeout = setTimeout(() => {
    subtitleElement.innerHTML = '';
  }, 5000);
});

socket.on('processing_error', (error) => {
  subtitleElement.innerHTML = `<div class="error">${error}</div>`;
});

// Cleanup
window.addEventListener('beforeunload', () => {
  mediaStream?.getTracks().forEach(t => t.stop());
  socket.disconnect();
});