from easyfly.parsers import CSVParser, CSVDataFormat, PathLike
from pathlib import Path
import numpy as np

# _AIRLINES_CSV_FORMAT = CSVDataFormat(
#         airline=str,
#         speed=float,
#         fuel_factor=float,
#         ticket_price_factor=float,
#     )

# Functions specific to parsing CSV files in the "Airports.csv" format
class AirlinesParser(CSVParser):

    def __init__(self):
        self.format = _AIRLINES_CSV_FORMAT


    def read_as_dict(self, path: str | PathLike[str], header: bool = False) -> tuple:

        if path is not PathLike[str]:
            path = Path(path)

        csv_lines_as_dicts = self._read_csv_as_dict(path, self.format, header)
        return csv_lines_as_dicts
