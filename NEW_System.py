from collections import deque
from numpy import random
from FES__class import FES
from Queue__class import Queue
from SimResults__class import SimResults
from Patient__class import Patient
from Event__class import Event
from Distribution__class import Distribution
from Facility_System_NEW__class import Facility

from AveragedResults_Class import AveragedResults
import time
from scipy import stats

# simulation parameters
TYPE_1_SCAN_TIME_MEAN = 1557.57888               # 0.4326608 * 3600 = estimated fraction part 1 times nr. seconds in hour
TYPE_1_SCAN_TIME_SD = 351.987264                 # 0.09777424*3600
TYPE_2_SCAN_TIME_MEAN = 2409.62004               # 0.6693389*3600
TYPE_2_SCAN_TIME_SD = 674.22924                  # 0.1872859*3600
TYPE_1_TIME_BETWEEN_ARRIVALS_MEAN = 1825.45344   # 0.5070704*3600
LAMBDA_NORM_TYPE_1 = 1.972113
TYPE_2_TIME_BETWEEN_ARRIVALS_MEAN = 3065.19084   # 0.8514419*3600
TYPE_2_TIME_BETWEEN_ARRIVALS_STD = 1100.41596    # 0.3056711*3600
ALFA_GAMMA_TYPE_2 = 12.77268
BETA_GAMMA_TYPE_2 = 1/19.08253



class Simulation:
    def __init__(self, arrivalrate1, arrivalrate2, scantime1, scantime2, sched_scan_t1, sched_scan_t2):  # inserting all the distributions used in the simulation
        self.arrivalrate1 = arrivalrate1
        self.arrivalrate2 = arrivalrate2
        self.scantime1 = scantime1
        self.scantime2 = scantime2
        self.patient_counter = 0
        self.sched_scan_t1 = sched_scan_t1
        self.sched_scan_t2 = sched_scan_t2
        self.Duration_day = 22*60*60
        self.Duration_workday = 9*60*60
        self.Day_counter = 1
        self.time_last_departure = 0
        self.last_change_over_time_f1 = 0
        self.last_change_over_time_f2 = 0


    def simulate(self, T):

        t = 0
        fes = FES()                                                     # Initialize future event list
        f1 = Facility()                                                 # Facility for patient type 1
        f2 = Facility()                                                 # Facility for patient type 2

        # patient type 1
        a1 = self.arrivalrate1.rvs()
        p1 = Patient(a1, 1)                                             # Initialize first patient type 1
        firstEventp1 = Event(Event.CALL, a1, p1)                        # Initialize first call event patient type 1
        fes.add(firstEventp1)                                           # Add the event to the future event set

        # patient type 2
        stop = False
        while stop == False:
            a2 = self.arrivalrate2.rvs()                                                                 
            if a2 > 0:
                stop = True
        p2 = Patient(a2, 2)                                             # Initialize first patient type 2
        firstEventp2 = Event(Event.CALL, a2, p2)                        # Initialize first call event patient type 2
        fes.add(firstEventp2)                                           # Add the event to the future event set

        change_over = Event(Event.CHANGE, t + self.Duration_day - 1)    # Initialize first change of day event
        fes.add(change_over)                                            # Add the event to the future event set

        queue1 = Queue()                                                # Create instance of queue 1
        queue2 = Queue()                                                # Create instance of queue 2
        Queue_overview = deque()
        Queue_overview.append(queue1), Queue_overview.append(queue2)
        res = SimResults(queue1, queue2)

        while t < T:
            e = fes.next()                                              # Find the next event
            t = e.time                                                  # Find the time for the current event
            p = e.patient                                               # Find the patient for the current event

            if e.type == Event.CHANGE:
                res.frac_overtime.append(self.time_last_departure % self.Duration_day > self.Duration_workday)      # Save whether there was overtime on a day
                if self.last_change_over_time_f1 % self.Duration_day - self.Duration_workday > 0:                   # If there was overtime for f1
                    overtime = self.last_change_over_time_f1 % self.Duration_day - self.Duration_workday            # The duration of the overtime
                    res.busy_time_f1 -= overtime                                                                    # Substract it from the total busy time of f1
                    res.time_overtime.append(overtime)                                                              # Save the duration of the overtime

                else:                                                                                               # If there was no overtime, there was idle time. Add to total
                    res.idle_time_f1 += ((self.Duration_day*(self.Day_counter-1) + self.Duration_workday) - self.last_change_over_time_f1)

                if self.last_change_over_time_f2 % self.Duration_day - self.Duration_workday > 0:                   # If there was overtime for f2
                    overtime = self.last_change_over_time_f2 % self.Duration_day - self.Duration_workday            # The duration of the overtime

                    res.busy_time_f2 -= overtime                                                                    # Substract it from the total busy time of f2
                    res.time_overtime.append(overtime)                                                              # Save the duration of the overtime

                else:                                                                                               # If there was no overtime, there was idle time. Add to total
                    res.idle_time_f2 += ((self.Duration_day*(self.Day_counter-1) + self.Duration_workday) - self.last_change_over_time_f2)

                self.last_change_over_time_f1 = t+1                                                                 # Update value of last day change f1
                self.last_change_over_time_f2 = t+1                                                                 # Update value of last day change f2

                f1.new_day()                                                                                        # New day for facility 1
                f2.new_day()                                                                                        # New day for facility 2
                self.Day_counter+=1
                new_change = Event(Event.CHANGE, t + self.Duration_day)                                             # Create new event that we move to a next day
                fes.add(new_change)                                                                                 # Add the event to the future event set

            if e.type == Event.CALL:
                if p.patient_type == 1:

                    start_time_f1, end_time_f1 = f1.schedule_check(self.sched_scan_t1)                              # Check available time slot for f1
                    start_time_f2, end_time_f2 = f2.schedule_check(self.sched_scan_t1)                              # Check available time slot for f2

                    if start_time_f1 <= start_time_f2:                                                              # If available time slot at f1 is earlier than that of f2
                        start_time = start_time_f1                                                                  # Set start time to start time of appointment at f1
                        f1.schedule_facility(p, start_time_f1, end_time_f1)                                         # Schedule the time slot
                        p.moveTo(f1)                                                                                # Save that patient is scheduled for f1

                    else:                                                                                           # If available time slot at f2 is earlier than that of f1
                        start_time = start_time_f2                                                                  # Set start time to start time of appointment at f2
                        f2.schedule_facility(p, start_time_f2, end_time_f2)                                         # Schedule the time slot
                        p.moveTo(f2)                                                                                # Save that patient is scheduled for f2

                    sched = Event(Event.ARRIVAL, (self.Day_counter) * self.Duration_day + start_time, p)            # Create scheduled event
                    fes.add(sched)                                                                                  # Add the event to the future event set
                    
                    a = self.arrivalrate1.rvs()                                                                     # Find arrival time of new patient type 1
                    if t + a > (self.Day_counter - 1) * self.Duration_day + self.Duration_workday:                  # If patient calls after 17:00, move call to next day
                        time_left = t + a - ((self.Day_counter - 1) * self.Duration_day + self.Duration_workday)    # How much time patient called after 17:00
                        arrival_t = (self.Day_counter) * self.Duration_day + time_left                              # Set arrival time to time called after 17:00 the previous day
                        p = Patient(arrival_t, 1)                                                                   # Create new patient type 1
                        arr = Event(Event.CALL, arrival_t, p)                                                       # Create arrival event
                        fes.add(arr)                                                                                # Add the event to the future event set
                    else:
                        p = Patient(t + a, 1)                                                                       # Create new patient type 1
                        arr = Event(Event.CALL, t + a, p)                                                           # Create arrival event
                        fes.add(arr)                                                                                # Add the event to the future event set

                if p.patient_type == 2:
                    start_time_f1, end_time_f1 = f1.schedule_check(self.sched_scan_t2)                              # Check available time slot for f1
                    start_time_f2, end_time_f2 = f2.schedule_check(self.sched_scan_t2)                              # Check available time slot for f2

                    if start_time_f1 <= start_time_f2:                                                              # If available time slot at f1 is earlier than that of f2
                        start_time = start_time_f1                                                                  # Set start time to start time of appointment at f1
                        f1.schedule_facility(p, start_time_f1, end_time_f1)                                         # Schedule the time slot
                        p.moveTo(f1)                                                                                # Save that patient is scheduled for f1

                    else:                                                                                           # If available time slot at f2 is earlier than that of f1
                        start_time = start_time_f2                                                                  # Set start time to start time of appointment at f2
                        f2.schedule_facility(p, start_time_f2, end_time_f2)                                         # Schedule the time slot
                        p.moveTo(f2)                                                                                # Save that patient is scheduled for f2
                        
                    sched = Event(Event.ARRIVAL, (self.Day_counter) * self.Duration_day + start_time,p)             # Create scheduled event
                    fes.add(sched)                                                                                  # Add the event to the future event set
                    stop = False
                    while stop == False:
                        b = self.arrivalrate2.rvs()                                                                 # Find arrival time of new patient type 2
                        if b > 0:
                            stop = True                                                                  
                    if t + b > (self.Day_counter - 1) * self.Duration_day + self.Duration_workday:                  # If patient calls after 17:00, move call to next day
                        time_left = t + b - ((self.Day_counter - 1) * self.Duration_day + self.Duration_workday)    # How much time patient called after 17:00
                        arrival_t = (self.Day_counter) * self.Duration_day + time_left                              # Set arrival time to time called after 17:00 the previous day
                        p = Patient(arrival_t, 2)                                                                   # Create new patient type 2
                        arr = Event(Event.CALL, arrival_t, p)                                                       # Create arrival event
                        fes.add(arr)                                                                                # Add the event to the future event set
                    else:
                        p = Patient(t + b, 2)                                                                       # Create new patient type 2
                        arr = Event(Event.CALL, t + b, p)                                                           # Create arrival event
                        fes.add(arr)                                                                                # Add the event to the future event set

            elif e.type == Event.ARRIVAL:
                if p.location == f1:                                                                                # For patients scheduled at f1
                    p.start_waiting_time = t                                                                        # Start weitingtime patient
                    if len(queue1.queue) == 0 and f1.status_busy == 0:                                              # If patient is only one in queue & f1 not busy
                        queue1.waitingtime_patient.append(t - p.start_waiting_time)                                 # End waitingtime patient
                        stop = False
                        while stop == False:
                            next_scantime = scantime1.rvs()
                            if next_scantime > 0:
                                stop = True
                        dep = Event(Event.DEPARTURE, t + next_scantime, p)                                          # New event, depature
                        fes.add(dep)                                                                                # Add to Future event list
                        f1.status_busy = 1                                                                          # Change status of f1 to busy (1)
                        res.idle_time_f1 += (t - self.last_change_over_time_f1)                                     # Add period of idle time to total idle time f1
                        self.last_change_over_time_f1 = t                                                           # Update time of last change of status

                    else:
                        queue1.queue.append(p)                                                                      # Add patient to queue of f1

                if p.location == f2:                                                                                # For patients scheduled at f2
                    p.start_waiting_time = t                                                                        # Start weitingtime patient
                    if len(queue2.queue) == 0 and f2.status_busy == 0:                                              # If patient is only one in queue & f2 not busy
                        queue2.waitingtime_patient.append(t - p.start_waiting_time)                                 # End waitingtime patient
                        dep = Event(Event.DEPARTURE, t + (scantime2.rvs()*3600), p)                                 # New event, depature
                        fes.add(dep)                                                                                # Add to Future event list
                        f2.status_busy = 1                                                                          # Change status of f2 to busy (1)
                        res.idle_time_f2 += (t - self.last_change_over_time_f2)                                     # Add period of idle time to total idle time f2
                        self.last_change_over_time_f2 = t                                                           # Update time of last change of status
                    else:
                        queue2.queue.append(p)                                                                      # Add patient to queue of f2

            elif e.type == Event.DEPARTURE:
                self.time_last_departure = t                                                                        # Save time of last patient departuring on a day
                if p.location == f1:                                                                                # For patients scheduled at f1
                    f1.status_busy = 0                                                                              # Change status of f1 to idle (0)
                    res.busy_time_f1 += (t - self.last_change_over_time_f1)                                         # Add period of busy time to total busy time f1
                    self.last_change_over_time_f1 = t                                                               # Update time of last change of status
                    if len(queue1.queue) >= 1:                                                                      # When still people in the queue
                        p2 = queue1.queue[0]                                                                        # Select next patient
                        queue1.waitingtime_patient.append(t - p2.start_waiting_time)                                # End waitingtime patient
                        queue1.queue.remove(p2)                                                                     # Remove that patient from the queue
                        if p2.patient_type == 1:                                                                    # If next patient is of type 1
                            stop = False
                            while stop == False:
                                next_scantime = scantime1.rvs()
                                if next_scantime > 0:
                                    stop = True
                            dep = Event(Event.DEPARTURE, t + next_scantime, p2)                                     # New event, depature
                        else:                                                                                       # If next patient is of type 2
                            dep = Event(Event.DEPARTURE, t + (scantime2.rvs()*3600), p2)                            # New event, depature
                        fes.add(dep)                                                                                # Add to Future event set
                        f1.status_busy = 1                                                                          # Change status of f1 to busy (1)

                if p.location == f2:                                                                                # For patients scheduled at f2
                    f2.status_busy = 0                                                                              # Change status of f2 to idle (0)
                    res.busy_time_f2 += (t - self.last_change_over_time_f2)                                         # Add period of busy time to total busy time f2
                    self.last_change_over_time_f2 = t                                                               # Update time of last change of status
                    if len(queue2.queue) >= 1:                                                                      # When still people in the queue
                        p2 = queue2.queue[0]                                                                        # Select next patient
                        queue2.waitingtime_patient.append(t - p2.start_waiting_time)                                # End waitingtime patient
                        queue2.queue.remove(p2)                                                                     # Remove that patient from the queue
                        if p2.patient_type == 1:                                                                    # If next patient is of type 1
                            stop = False
                            while stop == False:
                                next_scantime = scantime1.rvs()
                                if next_scantime > 0:
                                    stop = True

                            dep = Event(Event.DEPARTURE, t + next_scantime, p2)                                     # New event, depature
                        else:                                                                                       # If next patient is of type 2
                            dep = Event(Event.DEPARTURE, t + (scantime2.rvs()*3600), p2)                            # New event, depature
                        fes.add(dep)                                                                                # Add to Future event set
                        f2.status_busy = 1                                                                          # Change status of f2 to busy (1)
        return res


def run_simulation(arrivalrate1, arrivalrate2, scantime1, scantime2, sched_scan_t1, sched_scan_t2, num_runs, limit):
    results_list = deque()

    for i in range(num_runs):
        print('Current Run: '+ str(i))
        print('time elapsed = ', time.time() - begin_time_1)
        sim = Simulation(arrivalrate1, arrivalrate2, scantime1, scantime2, sched_scan_t1, sched_scan_t2) 
        results_list.append(sim.simulate(22 * 60 * 60 * days))
        
    averaged_results = AveragedResults(results_list, days)
    averaged_results.createhistogram(averaged_results.total_q1_time, 25, 'New system: waiting time queue 1')
    averaged_results.createhistogram(averaged_results.total_q2_time, 25, 'New system: waiting time queue 2')
    averaged_results.createhistogram(averaged_results.total_total_time, 25, 'New system: waiting time both queues')
    averaged_results.createhistogram(averaged_results.total_time_overtime, 25, 'New system: overtime')

    return averaged_results

scantime1 = Distribution(stats.norm(loc=TYPE_1_SCAN_TIME_MEAN ,scale=TYPE_1_SCAN_TIME_SD)) 
scantime2 = Distribution(stats.gamma(ALFA_GAMMA_TYPE_2, scale=BETA_GAMMA_TYPE_2))
arrivalrate1 = Distribution(stats.expon(scale=TYPE_1_TIME_BETWEEN_ARRIVALS_MEAN))
arrivalrate2 = Distribution(stats.norm(loc=TYPE_2_TIME_BETWEEN_ARRIVALS_MEAN, scale=TYPE_2_TIME_BETWEEN_ARRIVALS_STD))
sched_scan_t1 = 1500 # = 25 min. TYPE_1_SCAN_TIME_MEAN rounded down to times 5 minutes.
sched_scan_t2 = 2400 # = 40 min

num_runs = 50
days = 365

begin_time_1 = time.time()
print(run_simulation(arrivalrate1, arrivalrate2, scantime1, scantime2, sched_scan_t1, sched_scan_t2, num_runs, days))
end_time_1 = time.time()
print('Scheduling System: New System')
print('Number of days: '+ str(days))
print('Number of runs: '+ str(num_runs), '\n')
elapsed_time_1 = end_time_1 - begin_time_1
print('Total Running time:', elapsed_time_1, '\n', '\n')
