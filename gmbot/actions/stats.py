from . import Action

import re
import random

class StatCheck(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 1:
            user = args[0]
            stat = args[1]
        else:
            user = context['user']
            stat = args[0]

        try:
            stats = state.get(chan, user)
        except KeyError:
            return "Unknown user"

        if stat in stats:
            result = stats[stat]
            return "%s has %s for %s" % (user, result, stat)
        else:
            return "Unknown stat"

    def help(self):
        return """Gets the value of a players stat.
    Usage: [user] [stat] or just [stat] if checking your own stats."""

class StatSet(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 2:
            user = args[0]
            stat = args[1]
            result = args[2]
        else:
            user = context['user']
            stat = args[0]
            result = args[1]

        state.set(chan,user,stat,result)
        return "%s has %s for %s" % (user, result, stat)

    def help(self):
        return """Sets the value of a players stat
    Usage: [user] [stat] [value] ([user] can be ommitted if changing your own stats)"""

class StatMod(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 2:
            user = args[0]
            stat = args[1]
            mod = args[2]
        else:
            user = context['user']
            stat = args[0]
            mod = args[1]

        try:
            result = int(state.get(chan,user,stat))
            result += int(mod)
        except ValueError:
            return "Bad modifier value."
        except KeyError:
            result = mod
        state.set(chan,user,stat,result)
        return "%s has %s for %s" % (user, str(result), stat)

    def help(self):
        return """Adds or subtracts from the value of a players stat
    Usage: [user] [stat] [+-n] ([user] can be ommitted if changing your own stats)"""
