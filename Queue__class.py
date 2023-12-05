from collections import deque

class Queue:
    def __init__(self,speed):
        self.queue = deque()                    #The actual queue
        self.waitingtime_patient = deque()     #Used to calculate the waiting time of a queue