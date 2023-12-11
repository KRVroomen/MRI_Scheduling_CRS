from collections import deque
from numpy import mean, std
import matplotlib.pyplot as plt

class AveragedResults:

    def __init__(self, results_list, days):
        self.results_list = results_list
        self.days = days

        # All items of different lists are appended to one big list & the mean and standard deviation of the big list values is taken.
        self.total_q1_time = [item for sublist in [r.queue1.waitingtime_patient for r in results_list] for item in sublist]
        self.mean_waitingtime_queue1 = mean(self.total_q1_time)
        self.std_waitingtime_queue1 = std(self.total_q1_time)
        self.max_waitingtime_queue1 = max(self.total_q1_time)

        # All items of different lists are appended to one big list & the mean and standard deviation of the big list values is taken.
        self.total_q2_time = [item for sublist in [r.queue2.waitingtime_patient for r in results_list] for item in sublist]
        self.mean_waitingtime_queue2 = mean(self.total_q2_time)
        self.std_waitingtime_queue2 = std(self.total_q2_time)
        self.max_waitingtime_queue2 = max(self.total_q2_time)

        # All items of different lists are appended to one big list & the mean and standard deviation of the big list values is taken.
        self.total_total_time = self.total_q1_time + self.total_q2_time
        self.mean_waitingtime_total = mean(self.total_total_time)
        self.std_waitingtime_total = std(self.total_total_time)
        self.max_waitingtime_total = max(self.total_total_time)

        # All busy time values divided by number of days (ex. first day) are appended to one big list & the mean of this big list is taken.
        self.total_busy_time_f1 = [r.busy_time_f1/(self.days-1) for r in results_list]
        self.mean_busy_time_f1 = mean(self.total_busy_time_f1)

        # All idle time values divided by number of days (ex. first day) are appended to one big list & the mean of this big list is taken.
        self.total_idle_time_f1 = [r.idle_time_f1/(self.days-1) for r in results_list]
        self.mean_idle_time_f1 = mean(self.total_idle_time_f1)

        # All busy time values divided by number of days (ex. first day) are appended to one big list & the mean of this big list is taken.
        self.total_busy_time_f2 = [r.busy_time_f2/(self.days-1) for r in results_list]
        self.mean_busy_time_f2 = mean(self.total_busy_time_f2)

        # All idle time values divided by number of days (ex. first day) are appended to one big list & the mean of this big list is taken.
        self.total_idle_time_f2 = [r.idle_time_f2/(self.days-1) for r in results_list]
        self.mean_idle_time_f2 = mean(self.total_idle_time_f2)

        # All fractional overtime values are appended to one big list & the mean of this big list is taken.
        self.total_frac_overtime = [r.frac_overtime for r in results_list]
        self.mean_frac_overtime = mean(self.total_frac_overtime)

        # All items of different lists are appended to one big list & the mean is taken if this big list is not empty, otherwise it takes value 0.
        self.total_time_overtime = [item for sublist in [r.time_overtime for r in results_list] for item in sublist] 
        self.mean_time_overtime = mean(self.total_time_overtime) if self.total_time_overtime else 0
    
    def createhistogram(self, hist_list, binss, title):  

        plt.hist(hist_list, bins = binss, rwidth = 0.8, density = True)
        plt.xlabel('Seconds')
        plt.ylabel('Density')
        plt.title(title)
        plt.show()

    def __str__(self):
        s = '-------------------------------------------------------------------' + '\n'
        s += '-------------------------------------------------------------------' + '\n'
        s += 'The Expected Waiting Time in Queue 1 = ' + str(round(self.mean_waitingtime_queue1/60,2)) + ' minutes.' + '\n'
        s += 'The Standard Deviation of the Waiting Time in Queue 1 = ' + str(round(self.std_waitingtime_queue1/60, 2)) + ' minutes.' + '\n'
        s += 'The Maximum Waiting Time in Queue 1 = ' + str(round(self.max_waitingtime_queue1/60,2)) + ' minutes.' + '\n'+ '\n'
        s += 'The Expected Waiting Time in Queue 2 = ' + str(round(self.mean_waitingtime_queue2/60, 2)) + ' minutes.' + '\n'
        s += 'The Standard Deviation of the Waiting Time in Queue 2 = ' + str(round(self.std_waitingtime_queue2/60, 2)) + ' minutes.' + '\n'
        s += 'The Maximum Waiting Time in Queue 2 = ' + str(round(self.max_waitingtime_queue2/60,2)) + ' minutes.' + '\n'+ '\n'
        s += 'The Expected Waiting Time in total = ' + str(round(self.mean_waitingtime_total/60, 2)) + ' minutes.' + '\n'
        s += 'The Standard Deviation of the Waiting Time in total = ' + str(round(self.std_waitingtime_total/60, 2)) + ' minutes.' + '\n'
        s += 'The Maximum Waiting Time in total = ' + str(round(self.max_waitingtime_total/60,2)) + ' minutes.' + '\n'
        s += '-------------------------------------------------------------------' + '\n'
        s += 'The Mean Busy Time Facility 1 = ' + str(round(self.mean_busy_time_f1/ 3600, 2)) + ' hours.' + '\n'
        s += 'The Mean Idle Time Facility 1 = ' + str(round(self.mean_idle_time_f1/ 3600, 2)) + ' hours.' + '\n'+ '\n'
        s += 'The Mean Busy Time Facility 2 = ' + str(round(self.mean_busy_time_f2 / 3600, 2)) + ' hours.' + '\n'
        s += 'The Mean Idle Time Facility 2 = ' + str(round(self.mean_idle_time_f2 / 3600, 2)) + ' hours.' + '\n'
        s += '-------------------------------------------------------------------' + '\n'
        s += 'The Fraction of overtime = ' + str(self.mean_frac_overtime) + '\n'
        s += 'The Mean time of overtime = ' + str(round(self.mean_time_overtime/ 60, 2)) + ' minutes' + '\n'
        s += '-------------------------------------------------------------------' + '\n'
        s += '-------------------------------------------------------------------' + '\n'
        return s