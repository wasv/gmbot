from __future__ import print_function
from gmbot.dispatcher import Dispatcher
import fileinput
import readline

try:
    input = raw_input
except NameError:
    pass

d = Dispatcher() # Create dispatcher.

while True:
    try:
        line = input('> ') # Read command
    except KeyboardInterrupt:
        print() # Add a newline and exit.
        break
    except EOFError:
        print() # Add a newline and exit.
        break
    print(d.dispatch('cli','cli',line)) # Dispatch and print command.
