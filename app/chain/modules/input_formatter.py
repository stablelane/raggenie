from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
import langdetect
from app.providers.query_translator.azure_translate import AzureTranslate

azure_client = AzureTranslate()

class InputFormatter(AbstractHandler):
    
    def detect_language(self, text):
        try:
            return langdetect.detect(text)
        except:
            return "en"

    async def handle(self, request: Any) -> str:
        logger.info("passing through => input_formatter")
        
        query = request.get('question', '')
        current_lang = self.detect_language(query)
        if current_lang != 'en':
            translated_text = azure_client.translate_api(query)
            request['lang'] = current_lang
            request['translated_text'] = translated_text
        else:
            request['lang'] = 'en'
        
        response = request
        return await super().handle(response)
