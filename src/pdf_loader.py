from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend


def load_pdf(pdf_file):
    try:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.images_scale = 2.0

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
                )
            }
        )

        result = doc_converter.convert(pdf_file)
        output = result.document.export_to_markdown()
        print(output)

        return output

    except Exception as e:
        print(f"Error during PDF conversion with Tesseract: {e}")
        raise
