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
        page_count = len(result.document.pages)
        output = result.document.export_to_markdown()
        
        print("=" * 30)
        print(f"이력서 페이지 수: {page_count}")
        print("이력서 Parsing 결과:")
        print(output)
        
        return {
            "resume": output,
            "pages": page_count
        }

    except Exception as e:
        print(f"Error during PDF conversion with Tesseract: {e}")
        raise
