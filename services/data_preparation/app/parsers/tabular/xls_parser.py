from io import BytesIO
from typing import Any

import pandas as pd


def parse_xls(
    file_stream: BytesIO,
) -> list[dict[str, Any]]:
    """
    Parse XLS file into records.
    """

    file_stream.seek(0)

    dataframe = pd.read_excel(
        file_stream,
        engine="xlrd",
    )

    dataframe = dataframe.where(
        dataframe.notna(),
        None,
    )

    return dataframe.to_dict(
        orient="records"
    )