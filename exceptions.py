# Exception thrown when the response from the API is not 200
class APIFailException(Exception):
    pass


# Exception thrown when file is not found
class ReadFileException(Exception):
    pass
