
class AutoAttributes:
	
	attrs = ()
	
	def __init__(self, **kwargs):
		"""Método construtor genérico"""

		for attr in self.attrs:
			if attr in kwargs:
				setattr(attr, kwargs[attr])

	def __repr__(self):
		body = [f"{attr}={getattr(self, attr, None)}" for attr in self.__table__.columns]
		return f"{self.__class__.__name__}({', '.join(body)})"

	def to_dict(self):
		return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
	
	def from_dict(self,data):
		for field in self.attrs:
			if field in data:
				setattr(self,field,data[field])