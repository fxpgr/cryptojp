def http_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            raise(e)
        except Exception as e:
            raise(e)
    return wrapper


class SymbolNotFound(Exception):
    pass
