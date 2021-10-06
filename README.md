# Installation

```bash
pip install PyCommands
```

# Usage

```py
import PyCommands
from PyCommands import commands

engine=commands.CommandMaker(prefix="!", name="Timmy", description="Timmy is an engine for making simple commands") #make the CommandMaker instance, Set prefix through prefix kwargs, and set name also description through the kwargs. 

@engine.command("hello", description="say hello to someone :)") #Set command name and the description
def hello(someone): #support args, as of rigth now PyCommands doesnt support kwargs.
    engine.response(f"hello {someone}") #function for printing msg

@engine.command("plus", description="Add numbers")
def plus(a:int, b:int): #make sure to typehinted!
    engine.response(a + b) #Will be called with !plus <number> <number>, and it will print the mathematical equation

engine.run() #Run the CommandMaker and make a loop, it will not break unless you use the exit command or rerun the file
```

# Links
You can make PR or open an issue in [Github](https://github.com/TheGenocides/PyCommands)

# Licence
[Mit](https://choosealicense.com/licenses/mit/)
