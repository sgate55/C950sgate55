from datetime import timedelta

class Truck:
    #These are constants across all trucks created
    packages_max = 16
    avg_speed = 18

    #Initializes the truck with all the input values listed.
    def __init__(self, truck_id, speed=avg_speed, packages_max=packages_max):
        self.id = truck_id
        self.package_ids = []
        self.speed = speed
        self.packages_max = packages_max
        self.total_distance = 0
        self.mile_times = []
        self.driver = None
        self.time = timedelta(hours=8, minutes=0, seconds=0)
        self.hub = "4001 South 700 East"
        self.in_hub = True

    #Assigns the input package to this truck
    def add_package(self, package):
        #If the truck is already full, do not add the package
        if len(self.package_ids) < self.packages_max:
            self.package_ids.append(package.pckg_id)
            package.truck_id = self.id
        else:
            return False

    #All packages on the truck will be set to "En route"
    def set_in_transit(self, hash_table):
        for package_id in self.package_ids:
            package = hash_table.lookup(package_id)
            package.status = "En route"
            package.out_timestamp = self.time

    #This method will deliver the package and edit values as needed
    def deliver(self, hash_table, package_id, distance):
        package = hash_table.lookup(package_id)
        self.package_ids.remove(package_id)
        self.in_hub = False
        self.add_distance(distance)
        self.time += timedelta(minutes=(distance / self.speed * 60))
        self.mile_times.append([self.total_distance, self.time])
        package.status = "Delivered"
        package.delivered_timestamp = self.time

    #Returns the truck to the hub and edits values as needed
    def return_to_hub(self, distance_to_hub):
        self.add_distance(distance_to_hub)
        if self.time is None:
            self.time = timedelta(hours=8, minutes=0, seconds=0)
        self.time += timedelta(minutes=(distance_to_hub / self.speed * 60))
        self.mile_times.append([self.total_distance, self.time])
        self.in_hub = True

    #Adds distance to the total distance the truck has traveled
    def add_distance(self, distance):
        self.total_distance = self.total_distance + distance

    #Creates and returns a list of all packages on the truck
    def get_packages(self, hash_table):
        packages = []
        for package_id in self.package_ids:
            packages.append(hash_table.lookup(package_id))

        return packages

    #Checks if the package is full, returns true if it is and false if it is not
    def check_full(self):
        if (len(self.package_ids)) == self.packages_max:
            return True
        return False