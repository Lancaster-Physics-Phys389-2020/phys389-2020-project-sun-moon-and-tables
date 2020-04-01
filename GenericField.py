class GenericFieldClass:
    """Parent class to external and point source EM fields

     __init__(self, name)
        Args:
            name (string): Name of the field
    """
    
    def __init__(self, name='Generic Field'):
        self.name = name

    def __repr__(self):
        return 'Field: {0}'.format(self.name)

    