import urllib.parse


class CatalogItemFilter:
    """A filter for catalog items based on column name and value.
    
    Args:
        column_name (str): The name of the column to filter on. Cannot be empty.
        value (str): The value to filter by. If empty, will be stored as empty string.
    
    Raises:
        ValueError: If column_name is not provided (empty or None).
    """
    def __init__(self, column_name, value):
        if not column_name:
            raise ValueError("Column name was not provided")

        self.column_name = column_name
        self.value = value if value else ""


class CatalogItemFilters:
    """A collection of CatalogItemFilter objects with optional wildcard support.
    
    Args:
        filters (list[CatalogItemFilter]): List of filter objects. Cannot be None.
        use_wildcard (bool, optional): Whether to use wildcard matching. Defaults to False.
    
    Raises:
        ValueError: If filters is None.
    
    Attributes:
        filters (list[CatalogItemFilter]): The list of CatalogItemFilter instances.
        use_wildcard (bool): Flag for wildcard matching.
    """
    def __init__(self, filters, use_wildcard=False):
        if filters is None:
            raise ValueError("Filters were not provided")
        self.filters = filters
        self.use_wildcard = use_wildcard

    def __str__(self):
        """String representation of all filters in URL query parameter format.
        
        Returns:
            str: URL-encoded filters concatenated with '&' as separator,
                 with optional wildcard flag. Returns empty string if no filters exist.
        """
        if not self.filters:
            return ""
            
        filter_strings = []
        for f in self.filters:
            encoded_column = urllib.parse.quote_plus(f.column_name)
            encoded_value = urllib.parse.quote_plus(f.value)
            filter_strings.append('column={0}&value={1}'.format(encoded_column, encoded_value))
        
        result = '&'.join(filter_strings)
        
        if self.use_wildcard:
            result += '&use_wildcard={0}'.format(self.use_wildcard)
        return result