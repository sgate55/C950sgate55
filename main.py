# August (Sadie) Gates
# WGU ID #011051957

import csv
from datetime import datetime, timedelta

from driver import Driver
from hash_map import HashTable
from package import Package
from truck import Truck

#The number of trucks and drivers as indicated in the document
truck_count = 3
driver_count = 2

#Gets information from packages.csv to fill the hash table.
def package_info(hash_table):
    #packages.csv is opened
    with open('packages.csv') as csv_current:
        #Reader is created, which goes through the open csv file
        reader = csv.reader(csv_current, delimiter=',')
        #Gets information from all rows for the package objects
        for row in reader:
            #Take the information and create a new package with it, then add it to the hash table
            pckg_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]
            status = "At delivery hub"
            package = Package (pckg_id, address, city, state, zip_code, deadline, weight, notes, status)
            hash_table.insert(package)

def address_info():
    #addresses.csv is opened
    with open('addresses.csv') as csv_current:
        address_list = []
        #Reader is created, which goes through the open csv file
        reader = csv.reader(csv_current, delimiter=',')
        #Gets information from all rows for the addresses
        for row in reader:
            #Only takes the street address from the file
            address = row[0].split("\n")
            street = address[1].strip()
            address_list.append(street)
    return address_list

#Gets information from distances.csv for use in the program
def distance_info():
    #distances.csv is opened
    with open('distances.csv') as csv_current:
        #Reader is created, which goes through the open csv file
        reader = csv.reader(csv_current, delimiter=',')

        #This list will store the data from the file
        address_count = get_address_count()
        distance_data = [[0 for x in range(address_count)] for y in range(address_count)]

        #Read through the file and take the distance information from it
        src_address_index = 0

        for src_address in reader:
            for destination_address_index in range(address_count):
                if src_address[destination_address_index] != '':
                    distance_data[src_address_index][destination_address_index] = float(src_address[destination_address_index])
                    distance_data[destination_address_index][src_address_index] = float(src_address[destination_address_index])
            src_address_index = src_address_index + 1

        return distance_data

#Calculates the travel distance between two addresses
def travel_distance(address1, address2):
    distance_list = distance_info()
    address_list = address_info()

    #Gets the index of each address
    address1_index = address_list.index(address1)
    address2_index = address_list.index(address2)

    #Uses the index of each address in the distance list to find the distance between the addresses
    return distance_list[address1_index][address2_index]

#Initializes the drivers and trucks
def truck_drivers_initializer(truck_count, driver_count):
    truck_list = []
    driver_list = []
    truck_driver_count = min(truck_count, driver_count)
    for current_truck in range(1, truck_driver_count + 1, 1):
        truck_id = current_truck
        truck = Truck(truck_id)
        truck_list.append(truck)

    for current_driver in range(1, truck_driver_count + 1, 1):
        driver_id = current_driver
        driver = Driver(driver_id)
        driver.set_truck(truck_list)
        driver_list.append(driver)

    return truck_list, driver_list

#Finds the number of addresses based on the rows in the csv file and returns this information
def get_address_count():
    address_count = 0
    #addresses.csv is opened
    with open('addresses.csv') as csv_current:
        reader = csv.reader(csv_current, delimiter=',')
        for row in reader:
            address_count = address_count + 1
    return address_count

#Finds the packages that must be delivered together with the assistance of find_grouped_packages
def get_grouped_packages(hash_table):
    grouped_lists = []
    for current in hash_table.packages:
        if current is not None and "Must be delivered with" in current.notes:
            grouped = find_grouped_packages(hash_table, current)
            combine = False
            to_combine = None
            if len(grouped_lists) > 0:
                for package in grouped:
                    for list in grouped_lists:
                        if package in list:
                            combine: True
                            to_combine: list
                            break
            if combine:
                for package in grouped:
                    if package not in to_combine:
                        to_combine.append(package)
            else:
                grouped_lists.append(grouped)
    return grouped_lists

#Finds the distance the truck has traveled at a prompted time
def distance_at_timestamp(truck_list, report_date):
    report_time = timedelta(hours=report_date.hour, minutes=report_date.minute)
    distance_total = 0
    for truck in truck_list:
        if len(truck.mile_times) > 0:
            index = len(truck.mile_times) - 1
            while index > 0:
                mile_time = truck.mile_times[index][0]
                timestamp = truck.mile_times[index][1]
                if timestamp <= report_time:
                    distance_total += mile_time
                    print("Truck %d's current mileage: %0.2f miles" % (truck.id, mile_time))
                    break
                else:
                    index = index - 1
            if index == 0:
                print("Truck %d's current mileage: %0.2f miles" % (truck.id, 0.00))
    report_time_str = str(report_time)
    print("\nThe total of all truck's mileage at " + report_time_str + " is %0.2f miles." % distance_total)

#Gives a report on a specific package, prompted by the user
def specific_package_report(hash_table, truck_list):
    report_time = time_prompter()
    pckg_id = package_id_prompter(hash_table)
    print("Finding package information at " + report_time.strftime("%I:%M %p"))
    display_package(hash_table, pckg_id, report_time)
    menu(hash_table, truck_list)

#Print statement that gives the information of a specific package
def display_package(hash_table, package_id, report_date):
    package = hash_table.lookup(package_id)
    report_time = timedelta(hours=report_date.hour, minutes=report_date.minute)
    if package is not None:
        package_status_string = "[ID = %d]" % package.pckg_id
        if package.out_timestamp > report_time:
            package_status_string += "\tStatus: At hub"
        elif package.delivered_timestamp > report_time:
            delivered_time = datetime.strptime(str(package.delivered_timestamp), "%H:%M:%S")
            package_status_string += "\tOut for delivery, should arrive at " + delivered_time.strftime("%I:%M %p")
        else:
            delivered_time = datetime.strptime(str(package.delivered_timestamp), "%H:%M:%S")
            package_status_string += "\tDelivered at " + delivered_time.strftime("%I:%M %p")

        package_status_string += "\tDelivery Address: " + package.address
        package_status_string += "\tDelivery City: " + package.city
        package_status_string += "\tDelivery Zip: " + package.zip_code
        package_status_string += "\tWeight of Package: " + package.weight
        package_status_string += "\tDeadline of Delivery: " + package.deadline

        print(package_status_string)


#Prompts the user to input a time for the report
def time_prompter():
    report_time = None

    while report_time is None:
        try:
            report_time = datetime.strptime(
                input("Input a time for the report in the following format [HOUR:MINUTE AM/PM]: "), "%I:%M %p")
        except:
            print("\tPlease follow the time format.\n")

    return report_time

#Prompts the user to input an id for the report
def package_id_prompter(hash_table):
    id = None
    while id is None:
        user_input = input("Enter the ID of the package in order to view it: ")
        if user_input.isdigit():
            if hash_table.lookup(int(user_input)) is not None:
                id = int(user_input)
            else:
                print("\tThe provided ID is not a package on record.\n")
        else:
            print("\tInvalid input.\n")
    return id

#Finds the packages that must be delivered together
def find_grouped_packages(hash_table, package):
    if "Must be delivered with" in package.notes:
        grouped = [package]
        notes_no_commas = package.notes.replace(",", " ")
        split_notes = notes_no_commas.split()
        package_ids = [int(i) for i in split_notes if i.isdigit()]
        for pckg_id in package_ids:
            package = hash_table.lookup(pckg_id)
            grouped.append(package)
            more_packages = find_grouped_packages(hash_table, package)
            if more_packages is not None:
                for more in more_packages:
                    if more not in grouped:
                        grouped.append(more)

        return grouped

#Print statement and control for the menu
def menu(hash_table, truck_list):
    print("--------------------")
    print("WGUPS")
    print("--------------------")
    print("Please select an option from below. \n")
    print("\t 1. Package Status")
    print("\t 2. Overall Report")
    print("\t 3. Exit")
    options = [1, 2, 3]
    choice = None

    #Requests user input for one of the available options
    while choice is None:
        user_input = input("\n Enter one of the above numbers as your choice: ")
        if user_input.isdigit() and int(user_input) in options:
            choice = int(user_input)
        else:
            print("The entered choice is not valid.")

    #Calls the needed methods depending on the user's choice
    if choice == 1: specific_package_report(hash_table, truck_list)
    if choice == 2: report(hash_table, truck_list)
    if choice == 3:
        print("Exiting program...")
        quit()

#Delivers all of the packages
def deliver_all(hash_table, truck_list):
    while not all_delivered(hash_table):
        for truck in truck_list:
            truck.set_in_transit(hash_table)
            current_location = truck.hub
            current_index = 0
            while len(truck.package_ids) > 0:
                pckg_id = truck.package_ids[current_index]
                package = hash_table.lookup(pckg_id)
                distance = travel_distance(current_location, package.address)
                truck.deliver(hash_table, pckg_id, distance)
                current_location = package.address
            truck.return_to_hub(travel_distance(current_location, truck.hub))
        for truck in truck_list:
            set_packages(hash_table, truck)

#Checks if all the packages have been delivered. If yes, returns true. If not, returns false.
def all_delivered(hash_table):
    for package in hash_table.packages:
        if package is not None and package.delivered_timestamp is None:
            return False
    return True

#Gets a list of any packages that have not yet been assigned to a truck
def get_packages_unassigned(hash_table):
    unassigned = []
    for package in hash_table.packages:
        if package is not None and package.truck_assigned_checker() is False:
            unassigned.append(package)
    return unassigned

#Gets a list of any packages that have not yet been assigned and are able to be assigned.
def get_able(hash_table, truck):
    unable = get_unable(hash_table, truck)
    able = []
    for package in get_packages_unassigned(hash_table):
        if package is not None and package not in unable:
            able.append(package)
    return able

#Gets a list of any packages that are not currently able to be assigned.
def get_unable(hash_table, truck):
    unable = []
    grouped_packages = get_grouped_packages(hash_table)
    for package in hash_table.packages:
        if package is not None:
            if package.truck_assigned_checker():
                unable.append(package)
            elif package.get_forced_truck_id() is not None and package.get_forced_truck_id() is not truck.id:
                unable.append(package)
                if len(grouped_packages) > 0:
                    for grouped in grouped_packages:
                        if package in grouped:
                            for grouped_package in grouped:
                                if grouped_package not in unable:
                                    unable.append(grouped_package)
            elif package.get_arrival_delay() is not None and package.get_arrival_delay() > truck.time:
                if package not in unable:
                    unable.append(package)
    return unable

#Print statements for the general report
def report(hash_table, truck_list):
    report_time = time_prompter()
    print("At " + report_time.strftime("%I:%M %p" + " the status of all of the packages is the following."))
    for package in range(1, len(hash_table.packages) + 1):
        if package is not None:
            display_package(hash_table, package, report_time)
    distance_at_timestamp(truck_list, report_time)
    menu(hash_table, truck_list)

#Assigns packages to the trucks and then calls sort_truck_packages to sort them by distance
def set_packages(hash_table, truck):
    while len(get_able(hash_table, truck)) > 0 and not truck.check_full() and truck.in_hub is True:
        if len(truck.package_ids) == 0:
            address = truck.hub
        else:
            truck_package_count = len(truck.package_ids)
            last_added_id = truck.package_ids[truck_package_count - 1]
            last_added = hash_table.lookup(last_added_id)
            address = last_added.address

        closest = find_closest(address, get_able(hash_table, truck))
        truck.add_package(closest)

        if closest.pckg_id == 9:
            closest.address = "410 S State St"
            closest.city = "Salt Lake City"
            closest.state = "UT"
            closest.zip_code = "84111"
            sort_truck_packages(hash_table, truck)

        for group in get_grouped_packages(hash_table):
            if closest in group:
                for grouped in group:
                    if grouped.truck_assigned_checker() is False:
                        truck.add_package(grouped)
        sort_truck_packages(hash_table, truck)

#Sorts the packages on a truck based on the distance between them, finding the shortest distances to put back to back
def sort_truck_packages(hash_table, truck):
    sorted = []
    address = truck.hub
    packages = truck.get_packages(hash_table)
    while len(packages) != 0:
        nearest = find_closest(address, packages)
        sorted.append(nearest.pckg_id)
        address = nearest.address
        packages.remove(nearest)
    truck.package_ids = sorted

#Finds the closest package to the current location
def find_closest(current_location, packages):
    closest = None
    closest_distance = None
    for package in packages:
        if package is not None:
            closest = package
            closest_address = closest.address
            closest_distance = travel_distance(closest_address, current_location)
        else:
            package_address = package.address
            package_distance = travel_distance(package_address, current_location)
            if package_distance < closest_distance:
                closest = package
                closest_distance = package_distance
    return closest

#Main method of the program, calling all methods as needed
def main():
    delivery_hash_table = HashTable()
    package_info(delivery_hash_table)
    truck_list, driver_list = truck_drivers_initializer(truck_count, driver_count)
    delayed_start = None
    for package in delivery_hash_table.packages:
        if package is not None and package.get_arrival_delay() is not None:
            if delayed_start is None or delayed_start > package.get_arrival_delay():
                delayed_start = package.get_arrival_delay()

    if len(truck_list) > 1:
        last_truck = len(truck_list) - 1
        truck_list[last_truck].time = delayed_start

    for truck in truck_list:
        set_packages(delivery_hash_table, truck)

    deliver_all(delivery_hash_table, truck_list)

    menu(delivery_hash_table, truck_list)

#Calls main and begins the program
main()