import asyncio
from .core import Command
from typing import Callable, Type, Set

class BaseCommandMaker():
	def __init__(self, prefix: str, **kwargs):
		self.prefix = prefix
		self.description=kwargs.get("description") or None
		self._commands_ = {}

	@property
	def commands(self) -> Set:
		return set(self._commands_.values())

	def _register_command(self, cmd):
		if not isinstance(cmd, Command):
			raise TypeError("That command isnt from the class 'Command' ")
		self._commands_[cmd.name] = cmd

	def command(self, name: str, cls: Type[Command] = Command, **kwargs) -> Callable:
		def decorator(func) -> Command:
			result = cls(func, name=name, **kwargs)
			self._register_command(result)
			return result
		return decorator
	
	def get_command(self, name: str) -> Command:
		result=self._commands_.get(name)
		return result or None
	


	def run(self):
		async def run_():
			while True:
				cmd: str = input("> ")
				if not cmd.startswith(self.prefix):
					print(f"Unknown prefix: {cmd[0]}")
				else:
					command=self.get_command(cmd.replace(self.prefix, " ").strip())
					if not command:
						print("Command not found!")
					else:
						await command.func()
		asyncio.run(run_())
			
class CommandMaker(BaseCommandMaker):
	pass
