from http.client import HTTPException


class GeccoBaseException(Exception):
    pass


class GeccoUserQuitException(GeccoBaseException):
    pass


class GeccoShellQuitException(GeccoBaseException):
    pass


class GeccoDataException(GeccoBaseException):
    pass


class GeccoGenericException(GeccoBaseException):
    pass


class GeccoSystemException(GeccoBaseException):
    pass


class GeccoFilePathException(GeccoBaseException):
    pass


class GeccoConnectionException(GeccoBaseException):
    pass


class GeccoThreadException(GeccoBaseException):
    pass


class GeccoValueException(GeccoBaseException):
    pass


class GeccoMissingPrivileges(GeccoBaseException):
    pass


class GeccoSyntaxException(GeccoBaseException):
    pass


class GeccoValidationException(GeccoBaseException):
    pass


class GeccoMissingMandatoryOptionException(GeccoBaseException):
    pass


class GeccoPluginBaseException(GeccoBaseException):
    pass


class GeccoPluginDorkException(GeccoPluginBaseException):
    pass


class GeccoHeaderTypeException(GeccoBaseException):
    pass


class GeccoIncompleteRead(HTTPException):
    def __init__(self, partial, expected=None):
        self.args = partial,
        self.partial = partial
        self.expected = expected

    def __repr__(self):
        if self.expected is not None:
            e = ', %i more expected' % self.expected
        else:
            e = ''
        return '%s(%i bytes read%s)' % (self.__class__.__name__,
                                        len(self.partial), e)

    def __str__(self):
        return repr(self)
