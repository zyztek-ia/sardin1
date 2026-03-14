import google.generativeai as genai
from flask import current_app

class GeminiService:
    def __init__(self):
        try:
            api_key = current_app.config.get('GEMINI_API_KEY')
        except RuntimeError:
            api_key = None

        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def get_unlock_commands(self, device_info, error_logs):
        if not self.model:
            return ["echo 'Gemini API Key not configured'"]
        prompt = f"As an expert technician, give me ADB commands for this device info: {device_info} and error: {error_logs}. Return ONLY commands, one per line."
        try:
            response = self.model.generate_content(prompt)
            return [cmd.strip() for cmd in response.text.strip().split('\n') if cmd.strip()]
        except:
            return ["echo 'Error querying Gemini'"]
