from datetime import datetime, timedelta

class Package:
    # Package's constructor, creates the object with the info passed into this method
    def __init__(self, pckg_id, address, city, state, zip_code, deadline, weight, notes, status):
        self.pckg_id = pckg_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.truck_id = None
        self.truck_status = False
        self.out_timestamp = None
        self.delivered_timestamp = None

    #If the package is currently on a truck, this function returns true
    def truck_assigned_checker(self):
        if self.truck_id is None:
            return False
        return True

    #If the package must be delivered on a specific truck, this method returns the id of this truck
    def get_forced_truck_id(self):
        if "Can only be on truck" in self.notes:
            #Assign the needed truck
            forced_truck_id = [int(i) for i in self.notes.split() if i.isdigit()][0]
            return  forced_truck_id
        return None

    #If the package will arrive late, this method will find and return the arrival time
    def get_arrival_delay(self):
        #Delays due to late arrival checker
        if "Delayed on flight---will not arrive to depot until" in self.notes:
            split_notes = self.notes.split()
            for split in split_notes:
                try:
                    time = datetime.strptime(split, "%H:%M")
                    arrival_delay_time = timedelta(hours=time.hour, minutes=time.minute)
                    return arrival_delay_time
                except:
                    pass
        #Delays due to wrong address checker
        if "Wrong address listed" in self.notes:
            arrival_delay_time = timedelta(hours=10, minutes=20)
            return arrival_delay_time
        return None

    #Gets the timedelta from the delivery deadline string and returns this value
    def get_deadline_time(self):
        split_notes = self.deadline.split()
        for split in split_notes:
            try:
                time = datetime.strptime(split, "%H:%M")
                deadline_time = timedelta(hours=time.hour, minutes=time.minute)
                return deadline_time
            except:
                pass