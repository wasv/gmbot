import gmbot.actions.roll as roll
import gmbot.actions.stats as stats
import gmbot.actions.items as items
from gmbot.jsonstore import JsonStore
import shlex

class Dispatcher(object):
    state = JsonStore() # Create persistent data store
    action_map = { # Mapping of command words to actions.
        "roll": roll.Roll,
        "stat": stats.StatCheck,
        "statget": stats.StatCheck,
        "statcheck":stats.StatCheck,
        "statset": stats.StatSet,
        "statmod": stats.StatMod,
        "inventory": items.Inventory,
        "obtain": items.InventoryAdd,
        "drop": items.InventoryRemove,
        }

    def dispatch(self, chan, user, message):
        """Parses and matches a message to a command.

        Args:
            chan(String): The chan that the message was sent in.
            user(String): The user that sent the message.
            message(String: The message that was sent.
        Returns: (String) Result of command.
        """
        args = shlex.split(message)
        if args[0] == "help": # Check for help keyword.
            if len(args) > 1:
                action = args[1]
            else:
                return "Commands:"+str([k for k in sorted(self.action_map.keys())])
            if action in self.action_map:
                return self.action_map[action]().help()
            else:
                return "No help for that action."
        elif args[0] in self.action_map: # Test if command exists in map
            action = args[0]
            context = {'user':user,'chan':chan}
            try:
                return self.action_map[action]().run(context, self.state, args[1:])
            except Exception as e:
                return repr(e)
        else:
            return "No such action."
