import asyncio
from typing import Callable, Type, Set, List, Dict, Union
from datetime import datetime
from PyCommands.__init__ import __version__
from .core import Command, InternalCommand, Color
from .constants import HELPCOMMAND, SUCCESS, DISABLED, TOO_MANY_ARGUMENTS, UN_COMMAND, EXIT

def _error_handler(command: str, arguments: List[str], error: Exception):
	if command == "help":
		if isinstance(error, AttributeError):
			print(Color.yellow() + f"[{UN_COMMAND}]: " + Color.red() + f"Unknown Command: {' '.join(arguments)}") 
		
		elif isinstance(error, TypeError):
			print(Color.yellow() + f"[{TOO_MANY_ARGUMENTS}]: " + Color.red() + f"Too many arguments passed for command '{command}': {' '.join(arguments)}")  

class BaseCommandMaker():
    def __init__(self, prefix: str, **kwargs):
        self.prefix = prefix
        self.name = kwargs.get("name") or "User101"
        self.description = kwargs.get("description") or None
        self._commands = {}
        self._internal_commands = {}
        self._error_cache_ = {} #Use this later...
        self.register_internal_command()
    
    @property
    def commands(self) -> Set:
        return set(self._commands.values())

    @property
    def internal_commands(self) -> Set:
        return set(self._internal_commands.values())

    @property
    def error_cache(self) -> Dict[int, str]:
        return self._error_cache_

    def register_command(self, command):
        if isinstance(command, Command):
            self._commands[command.name] = command
        else:
            raise TypeError("Command is not from 'Command' or 'InternalCommand' class")

    def command(self, name: str, *,description: str = None, cls: Type[Command] = Command, **kwargs) -> Callable: 
        if ' ' in name:
            raise TypeError("Command name cannot have space!")
        def decorator(func) -> Command: #Not supported: list, dict, typing.Union, typing.Optional. Supported: str, int
            result = cls(name, description=description, func=func, **kwargs)
            if self.get_internal_command(result.name) or self.get_command(result.name):
                raise TypeError("That command name is already exist!")
            self.register_command(result)
            return result
        return decorator

    def get_command(self, name: str):
        result=self._commands.get(name)
        return result or None

    def get_internal_command(self, command: str):
        internal_command=self._internal_commands.get(command)
        return internal_command or None

    def _internal_commands_(self):
        def _make_internal_command(name: str, description: str, func: List[Callable], cls: Type[InternalCommand] = InternalCommand) -> InternalCommand:
            new_command=cls(name, description, func)
            return new_command

        def _help() -> InternalCommand:
            command=_make_internal_command("help", "Return The HelpCommand", [lambda command: print(Color.white() + f'[{HELPCOMMAND}]: Status {HELPCOMMAND}. HelpCommand\n{self.get_command(command).description}')])
            return command

        def _exit() -> InternalCommand:
            command=_make_internal_command("exit", "Exit PyCommands Style Console", [lambda x: print(Color.red() + f'[{EXIT}]: Exit PyCommands Console, status: 0'), lambda x: exit()])
            return command

        return _help(), _exit()
		

    def register_internal_command(self):
        def add_internal_command(command: InternalCommand):
            self._internal_commands[command.name] = command

        for commands in self._internal_commands_(): 
            add_internal_command(commands)

    def response(self, *text: Union[str, int], color: Color = Color.white()):
        print(color + ''.join(text))

    def run(self):
        async def run_():
            print(Color.green() + f"[{SUCCESS}]: PyCommands {__version__} ({datetime.utcnow().strftime('%b %d, %Y')})\n. . .  Successfully Connected As {self.name}.\n. . .  Typein 'help <command>', for more info! type 'exit' to exit PyCommands style console.")
            while True:
                promt: str = input(Color.green() + f"[{SUCCESS}]: " + Color.blue() + ">>> ")
                cmd=promt.split(" ")[0]
                indexs=len(promt.split(" ")) - 1
                arguments=promt.split(" ")[-indexs:] if not indexs == 0 else [' ']
                if not cmd.startswith(self.prefix) or cmd is self.prefix: 	
                    if cmd.lower() in self._internal_commands.keys():
                        funcs=self.get_internal_command(cmd).func
                        for func in funcs:
                            try:
                                func(*arguments)
                            except Exception as e :
                                _error_handler(cmd, arguments, e)
                                break            		
                        
                else:
                    command=self.get_command(cmd.strip(self.prefix))
                    if not command:
                        print(Color.yellow() + f"[{UN_COMMAND}]: " + Color.red() + f"Unknown Command: {promt}"
                    )
                    else:
                        if command.disabled:
                            print(Color.yellow() + f"[{DISABLED}]: " + Color.red() + f"Disabled Command: {command.name}")
                            
                        else:
                            await command.invoke(*arguments)
                            
								
        asyncio.run(run_())

class CommandMaker(BaseCommandMaker):
    pass