# modules/language_detection.py
import requests
import json
import time
from typing import Dict, Optional

class LanguageDetection:
    def __init__(self, config):
        """Initialize language detection with Azure Cognitive Services."""
        self.api_key = config.get('api_key')
        self.endpoint = config.get('endpoint', 'https://api.cognitive.microsofttranslator.com')
        self.cached_language = None
        self.confidence_threshold = 0.7
        self.cache_expiry = 60  # Cache language detection for 60 seconds
        self.last_detection_time = 0
    
    async def detect_language(self, text: str) -> Dict:
        """Detect language of the given text."""
        # Return cached language for very short texts or if cache is recent
        if not text or len(text.strip()) < 10 or (time.time() - self.last_detection_time < self.cache_expiry and self.cached_language):
            return self.cached_language or {"language_code": "en", "confidence": 1.0}
        
        try:
            # Using Azure Text Analytics for language detection
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            body = {
                'documents': [
                    {
                        'id': '1',
                        'text': text
                    }
                ]
            }
            
            response = requests.post(
                f"{self.endpoint}/text/analytics/v3.1/languages",
                headers=headers,
                json=body
            )
            
            response_json = response.json()
            
            if (response.status_code == 200 and 
                'documents' in response_json and 
                len(response_json['documents']) > 0 and
                'detectedLanguage' in response_json['documents'][0]):
                
                detected_language = response_json['documents'][0]['detectedLanguage']
                confidence = detected_language['confidenceScore']
                
                if confidence > self.confidence_threshold:
                    self.cached_language = {
                        "language_code": detected_language['iso6391Name'],
                        "confidence": confidence
                    }
                    self.last_detection_time = time.time()
                    return self.cached_language
            
            # Return cached language if detection failed or had low confidence
            return self.cached_language or {"language_code": "en", "confidence": 1.0}
        
        except Exception as e:
            print(f"Language detection error: {str(e)}")
            return self.cached_language or {"language_code": "en", "confidence": 1.0}
