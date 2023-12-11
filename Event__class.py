class Event:
    CALL = 0
    ARRIVAL = 1
    DEPARTURE = 2
    CHANGE = 3

    def __init__(self, typ, time, pat=None):        # Function for creating an event
        self.type = typ
        self.time = time
        self.patient = pat

    def __lt__(self, other):
        return self.time < other.time
