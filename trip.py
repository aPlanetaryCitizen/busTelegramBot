from utility import Utility
class Trip:
    def __init__(self, code):
        self.code = code
        self.stopsids_times = []
        self.route_id = ''
        self.line = ''
        self.headsign = ''
        self.service_id = ''
        self.dates = []

    def to_text(self):
        result = f"trip id: {self.code} \nroute id: {self.route_id}\nline: {self.line}\n"
        for stop_time in self.stopsids_times:
            result += f"{stop_time[1]}     {stop_time[0]}\n"
        return result

    def time_by_stop(self, stop):
        for stop_time in self.stopsids_times:
            if stop_time[0] == stop:
                return stop_time[1]

    def stops_times(self):
        stops_times = []
        for stopid_time in self.stopsids_times:
            stops_times.append((Utility.get_stop(stopid_time[0]), stopid_time[1]))
        return stops_times

    def stop_by_time(self, time):
        for stop_time in self.stops_times():
            if stop_time[1] == time:
                return stop_time[0]


