import datetime
from arrival import Arrival
from utility import Utility
from geopy import distance


class Fermata:

    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.arrivals = []  # formato: (time, trip)
        self.alt_ids_names = []

    @staticmethod
    def lista_nomi_fermate(fermate):
        nomi_fermate = []
        for fermata in fermate:
            nomi_fermate.append(fermata.name)
        return nomi_fermate

    def to_text(self):
        return f"{self.id}    {self.name}"

    def add_arrival(self, time, trip):
        self.arrivals.append(Arrival(self.id, time, trip.code))

    def arrivals_in_time_range(self, time, minutes_range):
        result = []
        datetime_start = datetime.datetime.combine(datetime.date.today(), time)
        time_end = Utility.time_plus_delta(time, minutes_range)
        datetime_end = datetime.datetime.combine(datetime.date.today(), time_end)
        # print(f"{time}   {time_end}")

        for arrival in self.arrivals:
            if datetime_start < arrival.time < datetime_end:
                result.append(arrival)
        return result

    def arrivals_in_datetime_range(self, date_time, minutes_range):
        result = []
        datetime_end = date_time + datetime.timedelta(minutes=minutes_range)
        # print(f"{time}   {time_end}")

        for arrival in self.arrivals:
            if date_time < arrival.time < datetime_end:
                result.append(arrival)
        return result

    # usa un numero negativo in min_from_now per ottenere gli arrivi a partire da un orario precedente ad adesso
    def arrivals_in_minutes_range(self, minutes_from_now, minutes_range):
        start_datetime = datetime.datetime.now() + datetime.timedelta(minutes=minutes_from_now)
        return self.arrivals_in_datetime_range(start_datetime, minutes_range)


    def arrivals_now(self):
        return self.arrivals_in_minutes_range(20)

    def simplified_id(self):
        result = ''
        if '_' in self.id:
            result += self.id.split('_')[0]
        if '@' in self.id:
            index = self.id.find('@')
            result = self.id[index + 1:]


    def passing_lines(self):
        lines = []
        for arrival in self.arrivals:
            lines.append(arrival.get_trip().line)
        return Utility.remove_duplicates(lines)

    def get_info(self):
        info = ''
        info += f"coordinates: \n{self.latitude}, {self.longitude}\n"
        info += f"alt ids and names:\n"
        for i in range(len(self.alt_ids_names)):
            info += f"{self.alt_ids_names[i][0]}   {self.alt_ids_names[i][1]}\n"
        return info

    def dist_to(self, stop2):
        dist = distance.distance((self.latitude, self.longitude),(stop2.latitude, stop2.longitude)).m
        return dist

    def alt_ids(self):
        result = []
        for alt_id_name in self.alt_ids_names:
            result.append(alt_id_name[0])
        return result

    def alt_names(self):
        result = []
        for alt_id_name in self.alt_ids_names:
            result.append(alt_id_name[1])
        return result