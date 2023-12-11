from collections import deque
from numpy import mean
class SimResults():

    def __init__(self, queue1, queue2):                    # Queues are specified, such that the waiting times per queue can be checked.
        self.queue1 = queue1
        self.queue2 = queue2
        self.frac_overtime = deque()
        self.busy_time_f1 = 0
        self.idle_time_f1 = -32400                         # Idle time set to -32400 as there are no appointments yet on first day, only calls
        self.busy_time_f2 = 0
        self.idle_time_f2 = -32400
        self.time_overtime = deque()


    def WaitingTime_Q1(self):
        return (self.queue1.waitingtime_patient)           # These functions call the waiting_time lists of the Class queue

    def WaitingTime_Q2(self):
        return (self.queue2.waitingtime_patient)

    def calc_ratio(self):                                  # Function returning the mean of the fraction of overtime
        return mean(self.frac_overtime)


