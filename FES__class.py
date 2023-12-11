import heapq

class FES:

    def __init__(self):
        self.events = []

    def add(self, event):
        heapq.heappush(self.events, event)

    def next(self):
        return heapq.heappop(self.events)

    def isEmpty(self):
        return len(self.events) == 0

    def __str__(self):
        s = ''
        sortedEvents = sorted(self.events)
        for e in sortedEvents:
            s += str(e) + '\n'
        return s