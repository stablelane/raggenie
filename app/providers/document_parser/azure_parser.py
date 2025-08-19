from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from app.providers.config import configs
from loguru import logger
import fitz  # PyMuPDF
import io

class AzureParser:
    
    def __init__(self):
        self.endpoint = configs.azure_di_enpoint
        self.key = configs.azure_di_secret_key
        
    def document_ocr(self, path):
    
        metadata = {"path":path}
        doc = fitz.open(path)
        num_pages = doc.page_count
        out = []
        temp = {}
        for i in range(0, num_pages, 100):
            start_page = i + 1
            end_page = min(i + 100, num_pages)
            logger.info(f"Processing pages {start_page}-{end_page}") 
            pdf_writer = fitz.open()  # New in-memory PDF
            for j in range(i, min(i + 100, num_pages)):
                pdf_writer.insert_pdf(doc, from_page=j, to_page=j)
            
            # Save to bytes
            pdf_bytes = pdf_writer.write()
            pdf_writer.close()

            # Analyze with Azure Document Intelligence
            document_intelligence_client = DocumentIntelligenceClient(
                endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
            )
            poller = document_intelligence_client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=io.BytesIO(pdf_bytes),
                content_type="application/pdf",
                output_content_format=DocumentContentFormat.MARKDOWN
            )
            result = poller.result()
            if "content" not in temp:
                temp["content"] = []
            temp["content"].append(result.content)
            
        temp["metadata"] = metadata
        if len(temp["content"]) > 0:
                out.append(temp)
        return out