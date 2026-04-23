from os import PathLike
import csv
#from typing import TypeVar, Generic


class CSVParseError(Exception): 
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# TODO FIX RAISING ERRORS
class CSVParseFormatRowError(CSVParseError): 
    def __init__(self):
        self.message = "Fieldnames could not be infered. Is there a header in the CSV file ?"
        super().__init__(self.message)


class CSVParseOpenFileError(CSVParseError): 
    def __init__(self):
        self.message = "Could not format row of csv file. Perhaps header= or fieldnames= incorrectly specified?"
        super().__init__(self.message)


class CSVDataFormat(): 

    def __init__(self, **kwargs):
        self.__format = kwargs.copy()
    

    def get_header_names(self): return self.__format.keys()
    def get_types(self): return self.__format.values()


class CSVParser():

    def __init__(self, format: CSVDataFormat):
        self.format = format 

    
    def _open_csv_file(self, path: PathLike[str]):
        try:
            return open(path, mode='r', newline='')
        except IOError as ex:
            raise CSVParseOpenFileError from ex


    '''TODO MAKE DOC STRINGS'''
    '''
        If header bool is specified AND fieldnames are specified, we need to change what we pass into DictReader,
        as the default behaviour of the csv library is if fieldnames are passed, it includes the first line of the file.

        Imagine there is a header line present at the top of the file, but also fieldnames specified.
        The library will include the first line as valid data, which will make our list look funny.

        So instead if we specify header=True and fieldnames, the program will skip the first line!
        Otherwise just do normal behaviour (pass fieldnames).

    '''
    def _read_csv_as_dict(self, path: PathLike[str], format: CSVDataFormat, header: bool) -> list: 

        try:
        # newline='' must be specified according to the csv library
            with self._open_csv_file(path) as csvfile:
                
                skip_first_line = False
                if header:
                    skip_first_line = True
                    
                # Omit fieldnames= so it treats first line as header
                reader = csv.DictReader(csvfile, fieldnames=tuple(format.get_header_names()), dialect='excel')
                if skip_first_line: next(reader)

                if reader.fieldnames is None:
                    raise CSVParseFormatRowError

                res = list()
                types = tuple(format.get_types())
                for row in reader:
                    for i in range(len(types)):
                        row[reader.fieldnames[i]] = types[i](row[reader.fieldnames[i]])
                    res.append(row)

                return res          
            
        except ValueError as exc:
            raise CSVParseFormatRowError from exc

