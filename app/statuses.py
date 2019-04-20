__all__ = ['Up', 'Down', 'Unknown']


class Status:
    def __init__(self, code: int = 0):
        self.code = code

    def __repr__(self):
        return NotImplementedError


class Up(Status):
    def __repr__(self):
        return 'up'


class Down(Status):
    def __repr__(self):
        return 'down'


class Unknown(Status):
    def __init__(self, code: int = 0, extra: str = ''):
        super().__init__(code)
        self.extra = extra

    def __repr__(self):
        return 'unknown'
