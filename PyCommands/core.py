import asyncio
import random as ran
from colorama import Fore
from typing import List, Callable
from inspect import signature
from .constants import TOO_MANY_ARGUMENTS, FAILED

class Command():
    def __init__(self, name: str, *, description: str = None, func: Callable, **kwargs):
        self.name = name
        self.description = description or None
        self.func = func
        self.disabled = kwargs.get("disabled") or False

    @property 
    def arguments(self):
        sig=str(signature(self.func)).strip("(").strip(")").replace(",", " ").replace("*", " ").replace(":", " ").replace("int", " ").replace("str", " ").replace(" ", "")
        return sig if sig else None

    def __repr__(self):
        return "<Command: <name: {0.name} description: {0.description} disabled: {0.disabled} func: {0.func}>>".format(self)

    def disable(self):
        self.disabled = True

    async def injected(self, args):
        """Injected Typehintes to arguments."""
        injected=[]
        arguments={} 
        if self.arguments:
            for n, arg in enumerate(args):
                try:
                    ty=self.func.__annotations__.get(self.arguments[n])
                    arguments[self.arguments[n]] = (arg, ty if ty else type(arg))
                except IndexError:
                    print(Color.yellow() + f"[{TOO_MANY_ARGUMENTS}]: Too many arguments passed for command '{self.name}': {' '.join(args)}")
                    return 1
        
            for k, tup in arguments.items():
                try:
                    arg=tup[0]
                    tp=tup[1]
                    if type(arg) == tp:
                        injected.append(arg)

                    elif not type(arg) == tp:
                        injected.append(tp(arg))

                except ValueError as error:
                    print(Color.red() + f"[{FAILED}]: Failed to invoke '{self.name}': it raised an exception: {error}")
                    return 1

        
        if not injected:
            return 0
              
        else:
            return injected

    async def invoke(self, *args): 
        """Invoke the command with the given arguments"""
        injected=await self.injected(args)
        
        if not self.arguments and args:
            print(Color.yellow() + f"[{TOO_MANY_ARGUMENTS}]: Too many arguments passed for command '{self.name}': {' '.join(args)}")  
            return

        if injected == 1:
            return
            
        elif injected == 0:
            try:
                if asyncio.iscoroutinefunction(self.func):
                    await self.func()
                else:
                    self.func()
            except Exception as error:
                print(Color.red() + f"[{FAILED}]: Failed to invoke '{self.name}': it raised an exception: {error}")

        else:
            try:
                if asyncio.iscoroutinefunction(self.func):
                    await self.func(*injected)
                else:
                    self.func(*injected)
            except Exception as error:
                print(Color.red() + f"[{FAILED}]: Failed to invoke '{self.name}': it raised an exception: {error}")
            
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