import json

class JsonStore(object):
    fname = "store.json"
    data = {
        "defaultchan":
        {
            "username":{"key":42}
        },
        "otherchan":
        {
            "username":{"key":"value"}
        }
    }

    def __init__(self, fname=None):
        if fname:
            self.fname = fname
        self._load()
    
    def _load(self):
        try:
            with open(self.fname, 'r') as f:
                json.load(f)
        except:
            self._save()
    
    def _save(self):
        with open(self.fname, 'w') as f:
            json.dump(self.data, f)
    
    def get(self, chan=None, user=None, key=None):
        if chan is None:
            return self.data
        if user is None:
            return self.data[chan]
        if key is None:
            return self.data[chan][user]
        return self.data[chan][user][key]

    def set(self, chan, user, key, value):
        self.data[chan][user][key] = value
        self._save()
