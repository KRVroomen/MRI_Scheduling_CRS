# MRI_Scheduling_CRS

GENERAL IDEA:
A Discrete Event Simulation for the analysis of two scheduling policies.
For both systems two types of patients need to be scheduled in one of two MRI facilities.
Both types of patients have a different distribution in the duration of their scans.
When a patient calls to make an appointment, that patient must be scheduled at the day after the call.
Old scheduling policy schedules type 1 patients only in MRI facility 1, and type 2 on facility 2.
New scheduling policy schedules schedules both types of patients in both MRI facilities based on First Fit.
Both policies are set to simulate 365 days, 50 times.
