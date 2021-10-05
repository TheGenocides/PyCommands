import asyncio
from typing import List, Callable

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
        try:
            if asyncio.iscoroutinefunction(self.func):
                await self.func(*args)
            else:
                self.func(*args)
        except TypeError:
            if asyncio.iscoroutinefunction(self.func):
                await self.func()
            else:
                self.func()

class InternalCommand(Command): #This is for internal command like exit etc. You should be using class Command(): for making Command
    def __init__(self, name: str, description: str, func: List[Callable]):
        super().__init__(name, description=description, func=func, disabled=False)
        self.name = name
        self.description = description or None
        self.func = func

    def  __repr__(self):
        return "<InternalCommand: <name: {0.name} description: {0.description} func: {0.func}>>".format(self)