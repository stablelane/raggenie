from app.providers.document_parser.azure_parser import AzureParser
from app.providers.document_parser.docling_parser import DoclingParser
from loguru import logger

class ParserEngineLoader:
        
    def load_engine(self, unique_name):
        engine_class = {
            "azure": AzureParser,
            "docling": DoclingParser
        }
        
        # if unique_name == "docling":
        #     try:
        #         from app.providers.document_parser.docling_parser import DoclingParser
        #         engine_class["docling"] = DoclingParser
        #     except ImportError as e:
        #         logger.error(f"Failed to import DoclingParser: {e}")
        #         return None
        
        engine = engine_class.get(unique_name)
        if engine:
            try:
                en = engine()
                return en
            except Exception as e:
                raise e
            
        else:
            logger.warning("Invalid engine specified in configuration.")
            return None
            