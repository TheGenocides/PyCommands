import asyncio
import random as ran
from colorama import Fore
from typing import List, Callable
from .constants import TOO_MANY_ARGUMENTS, FAILED

class Command():
    def __init__(self, name: str, *, description: str = None, func: Callable, **kwargs):
        self.name = name
        self.description = description or None
        self.func = func
        self.disabled = kwargs.get("disabled") or False
        
    def __repr__(self):
        return "<Command: <name: {0.name} description: {0.description} disabled: {0.disabled} func: {0.func}>>".format(self)

    def disable(self):
        self.disabled = True

    async def invoke(self, *args):
        types=list(self.func.__annotations__.values())
        for arg in args:
            for type in types:
                try:
                    if type(arg) == type: #Check if you can make a string to integer, if not it will raised ValueError then it'll get catch with except. 
                        ...
 
                except ValueError as error:
                    print(Color.yellow() + f"[{FAILED}]: " + f"Failed to invoke '{self.name}': it raised an exception: {error}")
                    return
        try:
            if asyncio.iscoroutinefunction(self.func):
                await self.func(*args)
            else:
                self.func(*args)
        except TypeError:
            try:
                if asyncio.iscoroutinefunction(self.func):
                    await self.func()
                else:
                    self.func()
            except TypeError:
                print(Color.yellow() + f"[{TOO_MANY_ARGUMENTS}]: Too many arguments passed for command '{self.name}': {' '.join(args)}")            

class InternalCommand(Command): #This is for internal command like exit etc. You should be using class Command(): for making Command
    def __init__(self, name: str, description: str, func: List[Callable]):
        super().__init__(name, description=description, func=func, disabled=False)
        self.name = name
        self.description = description or None
        self.func = func

    def  __repr__(self):
        return "<InternalCommand: <name: {0.name} description: {0.description} func: {0.func}>>".format(self)

class Color():
	@classmethod
	def red(cls):
		return Fore.RED
	
	@classmethod
	def blue(cls):
		return Fore.BLUE
	
	@classmethod
	def yellow(cls):
		return Fore.YELLOW
	
	@classmethod
	def green(cls):
		return Fore.GREEN
	
	@classmethod
	def magenta(cls):
		return Fore.MAGENTA
	
	@classmethod
	def cyan(cls):
		return Fore.CYAN
	
	@classmethod
	def white(cls):
		return Fore.WHITE
	
	@classmethod
	def colors(cls):
		return [cls.red(), cls.blue(), cls.green(), cls.yellow(), cls.magenta(), cls.cyan(), cls.white()]
	
	@classmethod
	def random(cls):
		return ran.choice(cls.colors())

Colour=Color