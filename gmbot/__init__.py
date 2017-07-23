from gmbot.actions.roll import Roll
from gmbot.jsonstore import JsonStore

class Dispatcher(object):
    state = JsonStore()
    action_map = {
        "roll": Roll
        }

    def dispatch(self, user, room, message):
        args = message.split(' ')
        if args[0] == "help":
            action = args[1]
            if action in self.action_map:
                return self.action_map[action]().help()
            else:
                return "No help for that action."
        elif args[0] in self.action_map:
            action = args[0]
            return self.action_map[action]().run({'user':user,'room':room}, self.state, args[1:])
        else:
            return "No such action."
