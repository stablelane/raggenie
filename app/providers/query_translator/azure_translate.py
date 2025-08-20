from app.providers.config import configs
import requests
import uuid


class AzureTranslate:
    
    def __init__(self):
        self.endpoint = configs.azure_ts_endpoint
        self.key = configs.azure_ts_secret_key
        self.region = configs.azure_ts_region
    
    def translate_api(self, text):
        
        path = "/translate"
        constructed_url = f"{self.endpoint}{path}"

        params = {
            'api-version': '3.0',
            'from': 'ar',
            'to': ['en']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': f'{text}'
        }]

        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        result = response.json()[0].get('translations','')[0]
        translated_text = result.get('text', '')
        return translated_text
    