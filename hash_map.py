class HashTable:
    #Initializes the hash table with an initial size of 40.
    #This hash table uses linear probing.
    def __init__(self, init_size=40, c1=0, c2=1):
        self.init_size = init_size
        self.packages = [None] * init_size
        self.bucket_statuses = ["INITIAL_EMPTY"] * init_size

        self.c1 = c1
        self.c2 = c2

    #Adds a new item into the hash table, using the id of the item as the key and filling all data with the data of that id
    def insert(self, package):
        i = 0
        probed = 0
        N = len(self.packages)
        bucket = hash(package.pckg_id) % N

        #Iterates through the hash table and, upon finding an empty bucket, inserts the package into it
        while probed < N:
            if self.bucket_statuses[bucket] == "INITIAL_EMPTY" or self.bucket_statuses[bucket] == "PACKAGE_REMOVED":
                self.packages[bucket] = package
                self.bucket_statuses[bucket] = "IN_USE"
                return True

            #Increments i and finds the next bucket's index. Only used when an empty bucket has not yet been found
            i = i + 1
            bucket = (hash(package.pckg_id) + (self.c1 * i) + (self.c2 * i ** 2)) % N

            #Keeps track of how many buckets have been probed
            probed = probed + 1

        #Only used if no empty buckets exist in the hash table. Will increase the size of the hash table and then retry
        self.increase_size()
        self.insert(package)
        return True

    #Finds an item based on the given key. If it exists in the table, it is returned, otherwise it returns None.
    def lookup(self, key):
        i = 0
        probed = 0
        N = len(self.packages)
        bucket = hash(key) % N

        while (self.bucket_statuses[bucket] != "INITIAL_EMPTY") and (probed < N):
            if (self.packages[bucket] is not None) and (self.packages[bucket].pckg_id):
                return self.packages[bucket]

            #Increments i and finds the next bucket's index. Only used when the item has not yet been found
            i = i + 1
            bucket = (hash(key) + self.c1 * i + self.c2 * i ** 2) % N

            #Keeps track of how many buckets have been probed
            probed = probed + 1

        return None

    #Doubles the size of the hash table.
    def increase_size(self):
        #Creates a hash table that has double the capacity of the one that is being resized.
        increased_ht = HashTable(init_size=self.init_size * 2, c1=self.c1, c2=self.c2)

        #Copies the packages to the resized hash table
        for package in self.packages:
            increased_ht.insert(package)

        self.init_size = increased_ht.init_size
        self.packages = increased_ht.packages
        self.bucket_statuses = increased_ht.bucket_statuses

    #Print function
    def __str__(self):
        s = "   --------\n"
        index = 0
        for item in self.packages:
            value = str(item)
            if item is None: value = 'E'
            s += '{:2}:|{:^6}|\n'.format(index, value)
            index += 1
        s += "   --------"
        return s