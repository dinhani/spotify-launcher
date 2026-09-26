from collections import defaultdict
from typing import Callable

class TrackedDict[K, V]:
    def __init__(self, default: Callable[[], V]):
        self.data: defaultdict[K, V] = defaultdict(default)
        self.count: defaultdict[K, int] = defaultdict(int)

    def __getitem__(self, key: K) -> V:
        return self.data[key]

    def __setitem__(self, key: K, value: V):
        self.data[key] = value

    def get(self, key: K, default: V | None = None) -> V | None:
        if key in self.data:
            self.count[key] += 1
            return self.data[key]
        return default

    def untouched_keys(self) -> list[K]:
        return [key for key in self.data if self.count[key] == 0]