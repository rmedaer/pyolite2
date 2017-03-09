
class PyoliteException(Exception):
    """Abstract Pyolite exception."""
    pass

class ConfigurationFileException(PyoliteException):
    """Error raised when Pyolite2 could not read or write a configuration file."""
    pass

class PyoliteLexerException(PyoliteException):
    """Internal error raised by Pyolite2 lexer."""
    pass

class InvalidNameException(PyoliteException):
    """Error raised when Pyolite2 detect an invalid name."""
    pass

class RepositoryNotFoundException(PyoliteException):
    """Error raised when repository could not be found."""
    pass

class RepositoryDuplicateException(PyoliteException):
    """Error raised when Pyolite2 detect an duplicate of repository."""
    pass
