class Driver:
    # Initializes the driver class with the driver's ID and sets the assigned truck to none
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.truck = None

    #Sets the driver's assigned truck to a truck without an assigned driver
    def set_truck(self, trucks):
        for truck in trucks:
            if truck.driver is None:
                truck.driver = self
                self.truck = truck
                return True
        return False

    #Unassigns the driver's truck
    def remove_truck(self):
        self.truck.driver = None
        self.truck = None