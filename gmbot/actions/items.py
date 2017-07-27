from . import Action
inv_stat = 'items'
class Inventory(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 0:
            user = args[0]
        else:
            user = context['user']

        try:
            stats = state.get(chan, user)
        except KeyError:
            return "Unknown user"

        if 'items' in stats:
            result = stats['items']
            if result == []:
                return "%s has nothing in their inventory" % (user)
            return "%s has %s in their inventory" % (user, result)
        else:
            return "No inventory data for %s" % (user)

    def help(self):
        return """Lists a players inventory.
    Usage: [user] (can be ommitted to check your inventory)"""

class InventoryAdd(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 1:
            user = args[0]
            item = args[1]
        else:
            user = context['user']
            item = args[0]

        try:
            stats = state.get(chan, user)
        except KeyError:
            stats = {}

        if 'items' in stats:
            result = stats['items']
        else:
            result = []

        result.append(item)
        state.set(chan, user, 'items', result)
        return "%s has added %s to their inventory" % (user, item)

    def help(self):
        return """Adds an item to a players inventory.
    Usage: [user] [item] ([user] can be ommitted to check your inventory)"""

class InventoryRemove(Action):
    def run(self, context, state, args):
        chan = context['chan']
        if len(args) > 1:
            user = args[0]
            item = args[1]
        else:
            user = context['user']
            item = args[0]

        try:
            stats = state.get(chan, user)
        except KeyError:
            stats = {}

        if 'items' in stats:
            result = stats['items']
        else:
            result = []

        if item in result:
            result.remove(item)
        else:
            return "%s does not have a %s." % (user, item)

        state.set(chan, user, 'items', result)

        return "%s has removed %s from their inventory" % (user, item)

    def help(self):
        return """Removes an item from a players inventory.
    Usage: [user] [item] ([user] can be ommitted to check your inventory)"""
