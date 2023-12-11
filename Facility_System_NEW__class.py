import numpy as np
from collections import deque

class Facility:

    def __init__ (self):
        self.current_schedule_today = np.zeros(22*3600)                             # Initialize empty schedule for today.
        self.current_schedule_tomorrow = np.zeros(22*3600)                          # Initialize empty schedule for tomorrow.
        self.status_busy = 0                                                        # Initialize status of facility to 0 (not busy)

    def schedule_facility (self, patient, start_index, end_index):                  # Function to schedule a patient from given start time to given end time.
        self.current_schedule_tomorrow[start_index:end_index + 1] = patient.ID

    def schedule_check(self, scan_time):                                            # Function to check first available time slot for a patient for a facility.
        count = 0
        start_index = 0
        for n in range(len(self.current_schedule_tomorrow)):
            if self.current_schedule_tomorrow[n] == 0:
                count += 1
                if count == scan_time:
                    end_index = n
                    return start_index, end_index
            else:
                count = 0
                start_index = n + 1

    def new_day(self):                                                              # Function to execute schedule the next day.
        self.current_schedule_today = self.current_schedule_tomorrow.copy()
        self.current_schedule_tomorrow = np.zeros(22*3600)

