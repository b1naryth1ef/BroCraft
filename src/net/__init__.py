

class Buff(object):
    def __init__(self):
        self.data = list()

    def push(self, item):
        self.data.append(data)

    def push_multi(self, items):
        self.data += items

    def get_multi(self, count, shift=False):
        data = self.data[:count]
        if shift:
            self.lshift(count)
        return data

    def get(self, id=0, shift=False):
        if not self.has(id):
            return None
        data = self.data[id]
        if shift:
            self.lshift(1)
        return data

    def has(self, id):
        return id < len(self.data)

    def lshift(self, c):
        self.data = self.data[c:]

    def __len__(self):
        return len(self.data)
