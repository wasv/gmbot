class Action(object):
    def __init__(self):
        pass

    def run(self, context, state, args):
        """ Does the requested action

        Args:
            context(dict): contains the room and user where the command was called.
            state(JsonStore): a reference to the object store
            args(list<String>): any arguments passed to action
        """
        pass

    def help(self):
        """ Returns a helpful string """
        return "No help available"
