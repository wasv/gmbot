from gmbot.actions.roll import Roll
from gmbot.actions.stats import *
from gmbot.jsonstore import JsonStore

class Dispatcher(object):
    state = JsonStore() # Create persistent data store
    action_map = { # Mapping of command words to actions.
        "roll": Roll,
        "stat": StatCheck,
        "statget": StatCheck,
        "statcheck":StatCheck,
        "statset": StatSet,
        "statmod": StatMod,
        }

    def dispatch(self, chan, user, message):
        """Parses and matches a message to a command.

        Args:
            chan(String): The chan that the message was sent in.
            user(String): The user that sent the message.
            message(String: The message that was sent.
        Returns: (String) Result of command.
        """
        args = message.split(' ')
        if args[0] == "help": # Check for help keyword.
            if len(args) > 1:
                action = args[1]
            else:
                return "Commands:"+str([k for k in self.action_map.keys()])
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
