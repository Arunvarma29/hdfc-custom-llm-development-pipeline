from io import BytesIO
from typing import Callable, Any

from fastapi import HTTPException

from services.data_preparation.app.parsers.tabular.xlsx_parser import parse_xlsx
from services.data_preparation.app.parsers.tabular.csv_parser import parse_csv
from services.data_preparation.app.parsers.tabular.json_parser import parse_json
from services.data_preparation.app.parsers.tabular.xls_parser import parse_xls
from services.data_preparation.app.parsers.document.pdf_parser import parse_pdf
from services.data_preparation.app.parsers.document.txt_parser import parse_txt
from services.data_preparation.app.parsers.document.docx_parser import parse_docx




Parser = Callable[..., list[dict[str, Any]]]


PARSERS: dict[str, Parser] = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": parse_xlsx,
    "application/pdf": parse_pdf,
    "text/csv": parse_csv,
    "application/json": parse_json,
    "text/plain": parse_txt,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": parse_docx,
    "application/vnd.ms-excel": parse_xls,
}


def get_parser(content_type: str) -> Parser:
    parser = PARSERS.get(content_type)

    if parser is None:
        raise ValueError(
            f"No parser configured for content type: {content_type}"
        )


    return parser