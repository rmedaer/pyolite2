
class PyoliteException(Exception):
    """Abstract Pyolite exception."""
    pass

class ConfigurationFileException(PyoliteException):
    """Error raised when Pyolite2 could not read or write a configuration file."""
    pass

class PyoliteLexerException(PyoliteException):
    """Internal error raised by Pyolite2 lexer."""
    pass 
