from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
import langdetect
import requests
import uuid
import json



class InputFormatter(AbstractHandler):
    
    def detect_language(self, text):
        try:
            return langdetect.detect(text)
        except:
            return "en"
        
    def translate_api(self, text):
        endpoint = "https://api.cognitive.microsofttranslator.com"
        path = "/translate"
        constructed_url = f"{endpoint}{path}"

        params = {
            'api-version': '3.0',
            'from': 'ar',
            'to': ['en']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': 'SJwA00qlnxJx9AO4zVahIrU1XkenAFBuKomZS0mOgjcQ1DlqcUfJJQQJ99BGACF24PCXJ3w3AAAbACOG3ywr',
            'Ocp-Apim-Subscription-Region': 'uaenorth',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': f'{text}'
        }]

        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        result = response.json()[0].get('translations','')[0]
        language = result.get('to', '')
        translated_text = result.get('text', '')
        return translated_text, language
        

    async def handle(self, request: Any) -> str:
        logger.info("passing through => input_formatter")
        
        query = request.get('question', '')
        current_lang = self.detect_language(query)
        if current_lang != 'en':
            translated_text, lang = self.translate_api(query)
            request['lang'] = current_lang
            request['translated_text'] = translated_text
        else:
            request['lang'] = 'en'
        
        response = request
        return await super().handle(response)
