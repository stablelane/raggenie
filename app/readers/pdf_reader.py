from app.readers.docs_reader import DocsReader
from loguru import logger
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend

pipeline_options = PdfPipelineOptions()
pipeline_options.ocr_options = RapidOcrOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options, backend=DoclingParseV4DocumentBackend)
    }
)


class PDFLoader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            paths = self.source["path"]

            for path in paths:
                try:
                    metadata = {"path":path}
                    result = converter.convert(path)
                    temp = {}
                    temp["content"] = result.document.export_to_markdown()
                    temp["metadata"] = metadata
                    if len(temp["content"]) > 0:
                            out.append(temp)
                except Exception as e:
                    logger.error(e)
        return out


