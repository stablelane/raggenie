class DoclingParser:
    def __init__(self):
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
        from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend

        pipeline_options = PdfPipelineOptions()
        pipeline_options.ocr_options = RapidOcrOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=DoclingParseV4DocumentBackend,
                )
            }
        )

    def document_ocr(self, path):
        metadata = {"path": path}
        out = []
        temp = {}
        result = self.converter.convert(path)
        temp["content"] = result.document.export_to_markdown()
        temp["metadata"] = metadata
        if temp["content"]:
            out.append(temp)
        return out
