from easyfly.parsers import CSVParser, CSVDataFormat, PathLike, CSVParseError
from pathlib import Path
import numpy as np
import timeit

_AIRPORTS_CSV_FORMAT = CSVDataFormat(
        city=str,
        lat=float,
        long=float,
    )

_haversine_a = lambda phi1, phi2, lmda1, lmda2 : (np.pow(2, np.sin((phi2 - phi1) / 2)) + (np.cos(phi1) * np.cos(phi2) * np.pow(2, np.sin((lmda2 - lmda1) / 2))))
_haversine_c = lambda a : 2 * np.sqrt(np.atan2(a, 1 - a)) # maybe optimisation ? 
_haversine_c1 = lambda a : 2 * np.atan2(np.sqrt(a), np.sqrt(1 - a))


# Functions specific to parsing CSV files in the "Airports.csv" format
class AirportsParser(CSVParser):

    def __init__(self):
        self.format = _AIRPORTS_CSV_FORMAT
        self.csv_as_dicts = tuple[dict[str, str | float]]()
        self.city_names = tuple[str]()
        self.haversine_distance_matrix = None


    def _haversine_between_lats_longs(self, lambdas: float, phis: float):
        
        pass

    '''
        For each city, loop through all other cities and calculate the distance using haversine.
        Store the results in an N x N "adjacency matrix", representing distance between cities
    '''
    def __create_haversine_dist_matrix__(self): 
        if not self.csv_as_dicts: return

        city_names = list[str]()
        lat_long_coords = list[tuple[float, float]]()

        N = 0
        for (city, lat, long) in [d.values() for d in self.csv_as_dicts]:
            city_names.append(city)  # type: ignore
            lat_long_coords.append((lat, long)) # type: ignore
            N += 1

        city_names = tuple(city_names)

        difference = list[tuple[float, float]]()
        phi1and2 = list[tuple[float, float]]()
        for i in range(0, N):
            for j in range(i + 1, N): 
                phi1and2.append((lat_long_coords[i][0], lat_long_coords[j][0]))
                difference.append(self._subtract_tuple_helper(lat_long_coords[i], lat_long_coords[j]))

        hs = []
        

    # Subract t2 from t1 elementwise and store the result to 4dp.
    def _subtract_tuple_helper(self, t1: tuple[float, float], t2: tuple[float, float]) -> tuple[float, float]:
        return (round(t2[0] - t1[0], ndigits=4), round(t2[1] - t1[1], ndigits=4))

    def read_as_dict(self, path: str | PathLike[str], header: bool = False) -> tuple:

        if path is not PathLike[str]:
            path = Path(path)

        self.csv_as_dicts = tuple(self._read_csv_as_dict(path, self.format, header))
        self.__create_haversine_dist_matrix__()

        return self.csv_as_dicts
