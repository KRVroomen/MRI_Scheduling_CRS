import itertools

class Patient:
    id_obj = itertools.count(1)             # Call upon iterator function
    def __init__(self, arrival_time, patient_type):
        self.ID = next(Patient.id_obj)      # Create unique id for every patient
        self.arrival_time = arrival_time
        self.patient_type = patient_type
        self.start_waiting_time = 0         # The start for the waiting time for the patient is registered.
        self.location = 0                   # (Only used in New System) Location of patient initialized to 0 (not assigned to a facility yet)

    def moveTo(self, location):             # (Only used in New System) Function to move patient to facility where he/she is scheduled
        self.location = location


    def __str__(self):                      # Function to print a patient
        s = ""
        s = s + "Patient: " + str(round(self.arrival_time, 1))
        return s

