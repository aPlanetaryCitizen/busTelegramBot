
from utility import  Utility



class Arrival:

    def __init__(self, stop_id, time, trip_id):
        self.stop_id = stop_id
        self.time = time
        self.trip_id = trip_id

    def to_text(self):
        return f"{self.get_stop().id}    {self.get_trip().line}    {self.time}    {self.get_trip().code}    {self.get_trip().headsign}"

    def to_brief_text(self):
        return f"{self.get_trip().line}    {self.time.time()}"

    def get_trip(self):
        return Utility.get_trip(self.trip_id)

    def get_stop(self):
        return Utility.get_stop(self.stop_id)


