# Installation

```bash
pip install PyCommands
```

# Usage

```py
import PyCommands
from PyCommands import commands

engine=commands.CommandMaker(prefix="!", name="Timmy", description="Timmy is an engine for making simple commands") #make the CommandMaker instance, Set prefix through prefix kwargs, and set name also description through the kwargs. 

@engine.command("hello") #Set command name
def hello(): 
    print("Hello there!")

engine.run() #Run the CommandMaker and make a loop, it will not break unless you use the exit command or rerun the file
```

# Links
You can make PR or open an issue in [Github](https://github.com/TheGenocides/PyCommands)

# Licence
[Mit](https://choosealicense.com/licenses/mit/)