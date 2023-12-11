import numpy as np
from collections import deque

class Facility:

    def __init__ (self):
        self.current_schedule_today = np.zeros(22*3600)                                         # Initialize empty schedule for today.
        self.current_schedule_tomorrow = np.zeros(22*3600)                                      # Initialize empty schedule for tomorrow.
        self.status_busy = 0                                                                    # Initialize status of facility to 0 (not busy)

    def schedule_facility (self, patient, scan_time):                                           # Function to check open spot for patient & schedule him/her.
        count = 0
        start_index = 0
        for n in range(len(self.current_schedule_tomorrow)):
            if self.current_schedule_tomorrow[n] == 0:
                count += 1
                if count == scan_time:
                    end_index = n
                    self.current_schedule_tomorrow[start_index:end_index + 1] = patient.ID
                    return start_index
            else:
                count = 0
                start_index = n + 1

    def new_day(self):                                                                          # Function to execute schedule the next day.
        self.current_schedule_today = self.current_schedule_tomorrow.copy()
        self.current_schedule_tomorrow = np.zeros(22*3600)
