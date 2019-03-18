class PersistentEntryError(ValueError):

    def __init__(self):

        super(ValueError, self).__init__(
            'Datensatz kann nicht gelöscht werden, da persistent!')

class RelatedEntryError(ValueError):

    def __init__(self):

        super(ValueError, self).__init__(
            'Datensatz kann nicht gelöscht werden, da noch in Beziehung stehend!')

class MethodNotSupportedError(ValueError):

    def __init__(self, method):

        super(ValueError, self).__init__(
            'Not supported request method "{0}"!'
            .format(method))

class FunctionNotSupportedError(ValueError):

    def __init__(self, function):

        super(ValueError, self).__init__(
            'Not supported request function "{0}"!'
            .format(function))
