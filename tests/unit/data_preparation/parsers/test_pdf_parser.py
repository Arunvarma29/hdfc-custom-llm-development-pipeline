from io import BytesIO

from pypdf import PdfWriter

from services.data_preparation.app.parsers.document.pdf_parser import (
    parse_pdf,
)


def create_test_pdf() -> BytesIO:
    pdf = BytesIO()

    writer = PdfWriter()

    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)

    writer.write(pdf)

    pdf.seek(0)

    return pdf


def test_parse_pdf_returns_page_records():
    file_stream = create_test_pdf()

    records = parse_pdf(file_stream)

    assert len(records) == 2

    assert records[0]["page_number"] == 1
    assert records[1]["page_number"] == 2

    assert "content" in records[0]
    assert "content" in records[1]