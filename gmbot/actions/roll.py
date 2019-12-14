from . import Action

import re
import random

class Roll(Action):
    def run(self, context, state, args):
        if 'd' not in args[0]: # Checks for an invalid roll.
            return "Invalid roll %s, Syntax: ?d?+? where ? is a number." % (args[0])
        parts = re.split(r'd|\+',args[0]) # Split on 'd' or '+' character.
        qty = int(parts[0])
        sides = int(parts[1])
        if len(parts) > 2: # Check for modifier on roll.
            modifier = int(parts[2])
        else:
            modifier = 0

        result = modifier
        for i in range(0,qty): # Calculate result.
            result += random.randint(1,sides)

        return "%s rolled %d %d-sided dice with a bonus of %d and got %d" % (context['user'], qty, sides, modifier, result)

    def help(self): # Print help message
        return "Rolls dice. Usage: xdy+z where x is number of y-sided dice, with a +z bonus added."
