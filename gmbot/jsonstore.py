import json

class JsonStore(object):
    fname = "store.json" # default filename
    data = {} # The in-memory dictionary.

    def __init__(self, fname=None):
        if fname:
            self.fname = fname
        self._load()
    
    def _load(self):
        try:
            with open(self.fname, 'r') as f:
                self.data = json.load(f)
        except:
            self._save()
    
    def _save(self):
        with open(self.fname, 'w') as f:
            json.dump(self.data, f)
    
    def get(self, chan=None, user=None, key=None):
        if chan is None:
            return self.data
        if chan not in self.data:
            return {}

        if user is None:
            return self.data[chan]
        if user not in self.data[chan]:
            return {}

        if key is None:
            return self.data[chan][user]
        if key not in self.data[chan][user]:
            return {}

        return self.data[chan][user][key]

    def set(self, chan, user, key, value):
        if chan not in self.data:
            self.data[chan] = {}
        if user not in self.data[chan]:
            self.data[chan][user] = {}
        self.data[chan][user][key] = value
        self._save()
