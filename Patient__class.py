import itertools

class Patient:
    id_obj = itertools.count(1)
    def __init__(self, arrival_time, patient_type):
        self.ID = next(Patient.id_obj)
        self.arrival_time = arrival_time
        self.patient_type = patient_type
        self.start_waiting_time = 0  # The start for the waiting time for the customer is registered.
        self.location = 0  # The location of

    def moveTo(self, location):
        self.location = location

    def __str__(self):
        s = ""
        s = s + "Patient: " + str(round(self.arrival_time, 1))
        return s

