from app.readers.docs_reader import DocsReader
from loguru import logger


class PDFLoader(DocsReader):
    
    def load(self, engine):

        if "path" in self.source:
            paths = self.source["path"]

            for path in paths:
                try:
                    result = engine.document_ocr(path)
                    print(result)
                except Exception as e:
                    logger.error(e)
                    
        return result


