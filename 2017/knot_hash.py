import operator
import toolz


def knot_hash(s):
    kr = Knotter(s)
    kr.run()
    return kr.out


class Knotter:
    def __init__(self, s):
        self.s = s
        self.lengths = [ord(c) for c in s] + [17, 31, 73, 47, 23]
        self.pos = 0
        self.skip = 0
        self.cl = CircularList(range(256))
        self.size = len(self.cl)
        self.out = ""

    def knot(self, length):
        cl = self.cl
        pos = self.pos
        cl[pos : pos + length] = cl[pos : pos + length][::-1]
        self.pos = (pos + length + self.skip) % self.size
        self.skip += 1

    def round(self):
        for length in self.lengths:
            self.knot(length)

    def run(self):
        for _ in range(64):
            self.round()
        dense_hash = [
            toolz.reduce(operator.xor, x) for x in toolz.partition_all(16, self.cl)
        ]
        self.out = "".join([f"{i:0>2x}" for i in dense_hash])


class CircularList(list):
    """Thanks to https://stackoverflow.com/a/47606550/203629"""

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[x] for x in self._rangeify(key)]

        key = operator.index(key)
        if key < 0:
            raise IndexError("Negative indices not defined for CircularList")
        try:
            return super().__getitem__(key % len(self))
        except ZeroDivisionError:
            raise IndexError("Can't get an item from an empty CircularList")

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for k, v in zip(self._rangeify(key), value):
                self[k] = v
            return

        key = operator.index(key)
        if key < 0:
            raise IndexError("Negative indices not defined for CircularList")
        super().__setitem__(key % len(self), value)

    def _rangeify(self, slice_):
        start, stop, step = slice_.start, slice_.stop, slice_.step
        if start < 0 or stop < 0:
            raise IndexError("Negative indices not defined for CircularList")
        n = len(self)
        if start is None:
            start = 0
        start = start % n
        if stop is None:
            stop = len(self)
        else:
            stop = n
        if step is None:
            step = 1
        return range(start, stop, step)
