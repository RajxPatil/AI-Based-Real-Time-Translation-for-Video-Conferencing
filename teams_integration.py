# teams_integration.py
import os
import asyncio
import msal # type: ignore
import requests
import json
import time
import threading
import uuid
from dotenv import load_dotenv # type: ignore
from modules.realtime_subtitle_system import RealTimeSubtitleSystem
from modules.audio_capture import AudioCapture

load_dotenv()

class TeamsIntegration:
    def __init__(self):
        # Azure AD and Teams configuration
        self.client_id = os.getenv("TEAMS_APP_ID")
        self.client_secret = os.getenv("TEAMS_APP_PASSWORD")
        self.tenant_id = os.getenv("TEAMS_TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scopes = ["https://graph.microsoft.com/.default"]
        
        # Initialize MSAL app
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        # Initialize the subtitle system
        self.subtitle_system = RealTimeSubtitleSystem()
        self.access_token = None
        self.meeting_id = None
        self.call_id = None
        self.teams_audio_stream = None
        self.audio_capture = None
        self.refresh_token_thread = None
        self.is_running = False
        
    def initialize(self):
        """Initialize the Teams integration and subtitle system"""
        print("Initializing Teams integration...")
        
        # Get access token
        self.access_token = self._get_access_token()
        if not self.access_token:
            print("Failed to get access token")
            return False
        
        # Start token refresh thread
        self.is_running = True
        self.refresh_token_thread = threading.Thread(target=self._token_refresh_worker)
        self.refresh_token_thread.daemon = True
        self.refresh_token_thread.start()
        
        # Initialize subtitle system
        if not self.subtitle_system.initialize():
            print("Failed to initialize subtitle system")
            return False
        
        # Initialize audio capture
        self.audio_capture = AudioCapture()
        
        print("Teams integration initialized successfully")
        return True
        
    def _get_access_token(self):
        """Get Microsoft Graph API access token"""
        result = self.app.acquire_token_for_client(scopes=self.scopes)
        
        if "access_token" in result:
            print("Successfully acquired access token")
            return result["access_token"]
        else:
            print(f"Error getting token: {result.get('error')}")
            print(f"Error description: {result.get('error_description')}")
            return None
            
    def _token_refresh_worker(self):
        """Background worker to refresh the access token before it expires"""
        while self.is_running:
            # Refresh token every 50 minutes (tokens typically last 1 hour)
            time.sleep(3000)
            if self.is_running:
                print("Refreshing access token...")
                self.access_token = self._get_access_token()
                if not self.access_token:
                    print("Failed to refresh access token")
            
    def get_meetings(self):
        """Get list of scheduled meetings for the current user"""
        if not self.access_token:
            print("No access token available")
            return []
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                'https://graph.microsoft.com/v1.0/me/onlineMeetings',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('value', [])
            else:
                print(f"Error getting meetings: {response.status_code}")
                print(response.text)
                return []
        except Exception as e:
            print(f"Exception getting meetings: {str(e)}")
            return []
            
    def join_meeting(self, meeting_join_link):
        """Join a Teams meeting using Graph API"""
        if not self.access_token:
            print("No access token available")
            return False
            
        # Extract meeting ID from join link
        # Teams meeting links come in different formats
        try:
            if "meetup-join" in meeting_join_link:
                self.meeting_id = meeting_join_link.split("/")[-1].split("?")[0]
            elif "teams.microsoft.com/l/meetup-join" in meeting_join_link:
                # Example: https://teams.microsoft.com/l/meetup-join/19%3ameeting_ID%40thread.v2/0
                parts = meeting_join_link.split("/")
                for part in parts:
                    if "meeting_" in part or "meetup-join" in part:
                        self.meeting_id = part.split("?")[0]
                        break
            else:
                print("Could not parse meeting link format")
                return False
                
            if not self.meeting_id:
                print("Failed to extract meeting ID from link")
                return False
                
            print(f"Extracted meeting ID: {self.meeting_id}")
        except Exception as e:
            print(f"Error parsing meeting link: {str(e)}")
            return False
            
        # Join the meeting as a bot/service
        success = self._join_meeting_as_service()
        if not success:
            print("Failed to join meeting through Graph API")
            return False
            
        # Initialize audio capture for Teams
        if self.teams_audio_stream:
            self.audio_capture.initialize_teams_capture(self.teams_audio_stream)
        else:
            # Fallback to microphone capture
            print("No Teams audio stream available, falling back to microphone")
            self.audio_capture.initialize_microphone_capture()
            
        # Connect audio capture to the subtitle system
        self.audio_capture.set_audio_callback(self.subtitle_system._handle_audio)
        
        # Start the subtitle system
        self.subtitle_system.start()
        self.audio_capture.start_recording()
        
        print(f"Successfully joined meeting with ID: {self.meeting_id}")
        return True
        
    def _join_meeting_as_service(self):
        """Join a meeting as a service using Graph API"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Build the request to join the call
        payload = {
            "clientContext": str(uuid.uuid4()),
            "meetingInfo": {
                "onlineMeetingId": self.meeting_id
            },
            "mediaConfig": {
                "@odata.type": "#microsoft.graph.serviceHostedMediaConfig",
                "removeFromDefaultAudioGroup": False
            },
            "tenantId": self.tenant_id
        }
        
        try:
            response = requests.post(
                'https://graph.microsoft.com/v1.0/communications/calls',
                headers=headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.call_id = data.get('id')
                print(f"Successfully joined call with ID: {self.call_id}")
                
                # In a real implementation, you would subscribe to the call's audio stream
                # This is a simplified example
                self.teams_audio_stream = self._get_call_audio_stream()
                
                return True
            else:
                print(f"Error joining call: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"Exception joining call: {str(e)}")
            return False
            
    def _get_call_audio_stream(self):
        """Get the audio stream from a Teams call (simplified placeholder)"""
        # This is a placeholder for getting the real audio stream
        # In a real implementation, you would use the Teams Real-time Media Platform
        # or the Cloud Communications API to access the audio stream
        
        # For demonstration purposes, we'll create a mock audio stream
        class MockAudioStream:
            def __init__(self):
                self.is_active = True
                
            def read(self, chunk_size):
                # Simulate audio data - this would be real audio data in a real implementation
                if self.is_active:
                    # Return silence (all zeros)
                    return bytes(chunk_size * 2)  # 16-bit audio = 2 bytes per sample
                return None
                
            def close(self):
                self.is_active = False
                
        return MockAudioStream()
        
    def leave_meeting(self):
        """Leave the current Teams meeting"""
        if not self.meeting_id:
            print("Not in a meeting")
            return False
            
        # Stop the subtitle system
        if self.subtitle_system:
            self.subtitle_system.stop()
            
        # Stop audio capture
        if self.audio_capture:
            self.audio_capture.stop_recording()
            
        # Close Teams audio stream
        if self.teams_audio_stream:
            try:
                self.teams_audio_stream.close()
            except:
                pass
            self.teams_audio_stream = None
            
        # Terminate the call using Graph API
        if self.call_id and self.access_token:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
            }
            
            try:
                response = requests.delete(
                    f'https://graph.microsoft.com/v1.0/communications/calls/{self.call_id}',
                    headers=headers
                )
                
                if response.status_code in [200, 204]:
                    print(f"Successfully left call with ID: {self.call_id}")
                else:
                    print(f"Error leaving call: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"Exception leaving call: {str(e)}")
        
        print(f"Left meeting with ID: {self.meeting_id}")
        self.meeting_id = None
        self.call_id = None
        return True
        
    def set_target_language(self, language_code):
        """Set the target language for translation"""
        if self.subtitle_system and self.subtitle_system.translation:
            self.subtitle_system.translation.set_target_language(language_code)
            print(f"Target language set to: {language_code}")
            return True
        return False
        
    def get_supported_languages(self):
        """Get list of supported languages for translation"""
        if not self.access_token:
            return []
            
        headers = {
            'Ocp-Apim-Subscription-Key': os.getenv("AZURE_TRANSLATOR_KEY"),
            'Ocp-Apim-Subscription-Region': os.getenv("AZURE_TRANSLATOR_REGION")
        }
        
        try:
            response = requests.get(
                'https://api.cognitive.microsofttranslator.com/languages?api-version=3.0&scope=translation',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                languages = data.get('translation', {})
                # Convert to a simple list of language codes and names
                result = []
                for code, details in languages.items():
                    result.append({
                        'code': code,
                        'name': details.get('name')
                    })
                return result
            else:
                print(f"Error getting languages: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception getting languages: {str(e)}")
            return []
            
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up Teams integration...")
        self.is_running = False
        
        # Leave any active meeting
        if self.meeting_id:
            self.leave_meeting()
            
        # Clean up subtitle system
        if self.subtitle_system:
            self.subtitle_system.cleanup()
            
        # Clean up audio capture
        if self.audio_capture:
            self.audio_capture.cleanup()
            
        # Wait for token refresh thread to exit
        if self.refresh_token_thread and self.refresh_token_thread.is_alive():
            self.refresh_token_thread.join(timeout=1.0)
            
        print("Teams integration cleanup complete")
