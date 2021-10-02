import asyncio
from .core import Command
from typing import Callable, Type, Set
from colorama import Fore, Back, Style
from .constants import *

class BaseCommandMaker():
    def __init__(self, prefix: str, **kwargs):
        self.prefix = prefix
        self.name=kwargs.get("name") or None
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
            result = cls(name, func, **kwargs)
            self._register_command(result)
            return result
        return decorator
    
    def get_command(self, name: str) -> Command:
        result=self._commands_.get(name)
        return result or None

    def run(self):
        async def run_():
            print(Fore.GREEN + f"[{SUCCESS}]: Successfully Online As {self.name}. Using PyCommands Version 0.1.0!")
            while True:
                cmd: str = input(Fore.GREEN + f"[{SUCCESS}]: " + Fore.BLUE + ">>> ")
                if not cmd.startswith(self.prefix) or cmd is self.prefix: 	
                    if cmd.lower() == "exit()":
                        print(Fore.RED + f"[{EXIT}] Exited code, Status: None")
                        break
                
                else:
                    command=self.get_command(cmd.strip(self.prefix))
                    if not command:
                        print(Fore.YELLOW + f"[{UN_COMMAND}]: " + Fore.RED + f"Unknown Command: {cmd}"
                    )
                    else:
                        if command.disabled is True:
                            print(Fore.YELLOW + f"[{DISABLED}]: " + Fore.RED + f"Disabled Command: {cmd}")
                            
                        else:
                            await command.func()
                        
                        
        asyncio.run(run_())
            
class CommandMaker(BaseCommandMaker):
    pass
