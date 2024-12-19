class BookingForDisplay:
    def __init__(self, parking_garage_name, vehicle, start_time, end_time, status, id):
        self.parking_garage_name = parking_garage_name
        self.vehicle = vehicle
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.id = id

    @property
    def parking_garage_name(self):
        return self._parking_garage_name

    @parking_garage_name.setter
    def parking_garage_name(self, parking_garage_name):
        self._parking_garage_name = parking_garage_name

    @property
    def vehicle(self):
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle):
        self._vehicle = vehicle

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def __str__(self):
        return f'Vehicle: {self.vehicle}\nParking Garage: {self.parking_garage_name}\nStart Time: {self.start_time}\nEnd Time: {self.end_time}\nStatus: {self.status}'