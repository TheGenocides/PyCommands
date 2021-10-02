class Command():
	def __init__(self, func, *, name, disabled: bool = False, **fields):
		self.name = name
		self.func = func
		self.description = fields.get("description") or None
		self.disabled = fields.get("disabled") 
		
	def __repr__(self):
		return "<Command: <name: {0.name} description: {0.description} disabled: {0.disabled} func: {0.func}>>".format(self)

	def disable(self):
		self.disabled = False