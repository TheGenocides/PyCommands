# Installation

```bash
pip install PyCommands
```

# Usage

```py
import PyCommands
from PyCommands import commands

engine=commands.CommandMaker(prefix="!", name="Timmy", description="Timmy is an engine for making simple commands") #make the CommandMaker instance, Set prefix through prefix kwargs, and set name also description through the kwargs. 

@engine.command(description="say hello to someone :)") #Set command name and the description
def hello(someone): #support args, as of rigth now PyCommands doesnt support kwargs.
    engine.response(f"hello {someone}") #function for printing msg

@engine.command(description="Add numbers")
def plus(a:int, b:int): #make sure to typehinted!
    engine.response(a + b) #Will be called with !plus <number> <number>, and it will print the mathematical equation

engine.run() #Run the CommandMaker and make a loop, it will not break unless you use the exit command or rerun the file
```

Run the file, this is how to invoke the command in terminal.
```bash
[100]: PyCommands 0.3.2 (Oct 26, 2021)
. . .  Successfully Connected As Timmy.
. . .  Typein 'help <command>', for more info! type 'exit' to exit PyCommands style console.
[100]: >>> !hello world
Hello World
[100]: >>> !plus 100 123
223
[100]: >>> exit
[0]: Exit PyCommands Console, status: 0
```

# Links
You can make PR or open an issue in [Github](https://github.com/TheGenocides/PyCommands)

# Licence
[Mit](https://choosealicense.com/licenses/mit/)
