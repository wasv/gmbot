from . import Action

import re
import random

class Roll(Action):
    def run(self, context, state, args):
        if 'd' not in args[0]:
            return "Invalid roll %s, Syntax: ?d?+? where ? is a number." % (args[0])
        parts = re.split('d|\+',args[0])
        qty = int(parts[0])
        sides = int(parts[1])
        if len(parts) > 2:
            modifier = int(parts[2])
        else:
            modifier = 0

        result = modifier
        for i in range(0,qty):
            result += random.randint(1,sides)

        return "%s rolled %d %d-sided dice with a bonus of %d and got %d" % (context['user'], qty, sides, modifier, result)

    def help(self):
        return "Rolls dice. Usage: xdy+z where x is number of y-sided dice, with a +z bonus added."
