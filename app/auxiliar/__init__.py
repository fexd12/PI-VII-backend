
class AutoAttributes:
    attrs = ()

    def __init__(self, **kwargs):
        """Método construtor genérico"""
        for attr in self.attrs:
            if attr in kwargs:
                setattr(attr, kwargs[attr])

    def __repr__(self):
        body = [f"{attr}={getattr(self, attr, None)}" for attr in self.attrs]
        return f"{self.__class__.__name__}({', '.join(body)})"

    def to_dict(self):
        data = {}

        for attr in self.attrs:
            data[attr] = getattr(self, attr, None)

        return data
    
    def from_dict(self,data):
        for field in self.attrs:
            if field in data:
                setattr(self,field,data[field])
