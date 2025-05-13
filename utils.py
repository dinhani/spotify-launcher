from collections import defaultdict

class ProxyDict:
    def __init__(self, default):
        self.data = defaultdict(default)
        self.count = defaultdict(int)

    def __getitem__(self, key):
        self.count[key] += 1
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        if key in self.data:
            self.count[key] += 1
            return self.data[key]
        return default

    def untouched_keys(self):
        return [k for k in self.data if self.count[k] <= 1]