# modules/translation.py
import requests
import uuid
import json
from typing import Dict, Optional

class Translation:
    def __init__(self, config):
        """Initialize translation with Azure Translator."""
        self.api_key = config.get('api_key')
        self.endpoint = config.get('endpoint', 'https://api.cognitive.microsofttranslator.com')
        self.location = config.get('location', 'global')
        self.target_language = config.get('target_language', 'en')
    
    def set_target_language(self, language_code: str):
        """Set the target language for translation."""
        self.target_language = language_code
        print(f"Target language set to: {language_code}")
    
    async def translate_text(self, text: str, source_language: str) -> Dict:
        """Translate text from source language to target language."""
        if not text or not text.strip():
            return {'translated_text': '', 'original_text': text}
        
        # Don't translate if source and target are the same
        if source_language == self.target_language:
            return {'translated_text': text, 'original_text': text}
        
        try:
            # Using Azure Translator API
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Ocp-Apim-Subscription-Region': self.location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            body = [{
                'text': text
            }]
            
            params = {
                'api-version': '3.0',
                'from': source_language,
                'to': self.target_language
            }
            
            response = requests.post(
                f"{self.endpoint}/translate",
                headers=headers,
                params=params,
                json=body
            )
            
            response_json = response.json()
            
            if (response.status_code == 200 and 
                len(response_json) > 0 and 
                'translations' in response_json[0] and 
                len(response_json[0]['translations']) > 0):
                
                return {
                    'translated_text': response_json[0]['translations'][0]['text'],
                    'original_text': text
                }
            else:
                return {'translated_text': text, 'original_text': text}
        
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return {'translated_text': text, 'original_text': text}
