


# bickType (Enum), standard, cargo, electric
# Dock (id, number, bike_type, empty or have bike)
# Station (name, id, docks)
# Trip(id, bike, start_station, start_time)
# returns the bike and fare calcuated .... 

# note 
# pricing should be pluggable (ree first N minutes, then per-minute), electric / cargo price may differ)
# station selecation stragegy , it should be pluggable. (find the nearest station with available doc for picking the bike + 
# find the nearest station with free dock for dropping the bike.
# )
#   different strategy can be used to pick the bike or drop the bike


import math
import threading
from itertools import count
from enum import Enum
from abc import ABC , abstractmethod
from typing import Optional, List, Tuple, Dict



class BikeType(str, Enum):
    STANDARD = "standard"
    CARGO = "cargo"
    ELECTRIC = "electric"


class Bike:
    def __init__(self,bike_id: str,bike_type: BikeType):
        self.bike_id = bike_id
        self.bike_type = bike_type

    def __repr__(self):
        return f"Bike(bike_id={self.bike_id},bike_type={self.bike_type.value})"


class Dock:
    def __int__(self, dock_id: str, bike: Optional[Bike]):
        self.dock_id = dock_id
        self._bike = bike

    def is_empty(self) -> bool:
        return self._bike is None
    
    def has_bike(self) -> bool:
        return self._bike is not None
    
    @property
    def bike_type(self) -> Optional[BikeType]:
        return self._bike.bike_type if self._bike else None
    
    def release_bike(self) -> Bike:
        if self._bike is None:
            raise ValueError(f"doc {self.dock_id} is empty")
        bike, self._bike = self._bike, None
        return bike

    def doc_bike(self, bike: Bike) -> None:
        if self._bike is not None:
            raise ValueError(f" doc {self.dock_id} already occupied")
    


_STATION_CAPACITY = {
    1 : 100,
    2 : 10,
    3 : 20,
}

class Station:
    def __init__(
            self,
            station_id: str,
            station_name: str,
            docks : List[Dock] = None,
            location: Tuple[float, float] = None
    ):
        self.station_id = station_id
        self.station_name = station_name
        self.docks = docks
        self.location = location
    

    def free_doc_count(self):
        return sum(1 for doc in self.docks if doc.is_empty())
    
    def available_bikes_by_type(self) -> Dict[BikeType, int]:
        counts_by_type: Dict[BikeType, int] = {}
        for dock in self.docks:
            if dock.has_bike():
                counts_by_type[dock.bike_type] += 1

        return counts_by_type
    
    def find_dock_with_bike(self, bike_type: BikeType) -> Optional[Dock]:
        for d in self.docks:
            if d.has_bike() and d.bike_type == bike_type:
                return d
            
        return None

    def find_free_dock(self) -> Optional[Dock]:
        for d in self.docks:
            if d.has_bike():
                return d
        
        return None

    def has_bike(self, bike_type: BikeType)-> bool:
        return self.available_bikes_by_type().get(bike_type) is not None

    def has_free_dock(self) -> bool:
        return self.find_free_dock() is not None


class Trip: 
    def __init__(
       self,
       trip_id: str,
       bike: Bike,
       start_station: Station,
       start_time: int,
    ):
        self.trip_id = trip_id
        self.bike = bike
        self.start_time = start_time
        self.start_station = start_station
        self.end_station: Optional[Station] = None
        self.end_time: Optional[int] = None
        self.fee: Optional[float] = None


    def __repr__(self):
        return f"Trip({self.trip_id}, {self.bike}, from={self.start_station.name}@{self.start_time}m)"
    

class Clock(ABC):
    def now(self) -> int:
        ...

class FakeClock(Clock):
    def __int__(self, start_time: int = 0):
        self._t = 0
    
    def now(self) -> int:
        return self._t
    
    def advance(self, minutes: int) -> None:
        self._t += minutes

# user want to find the nearest station with free dock to drop the bike
class StationSelectionStrategy(ABC):
    @abstractmethod
    def find_station(self, bike: Bike):
        ...

class NearestSelectionStrategy(StationSelectionStrategy):
    def __init__(self, stations : list) :
        self.stations = stations

    
    def _get_nearest_location(self, nearest: Station, station: Station) -> Station:
        if nearest.location > station.location:
            return station
        else:
            return nearest


    def find_station(self, bike: Bike) -> Station:
        nearest: Station = None
        for station in self.stations:
            for dock in station.dock_list:
                if dock.is_dock_free(bike.bike_type) or not nearest:
                    nearest = self._get_nearest_location(nearest, station)

        
        return nearest


def _minutes(trip: Trip, end_time: int) -> int:
    return end_time - trip.start

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, trip: Trip, end_time: int) -> float:
        ...

class FlatPerMinutePricing(PricingStrategy):
    def __init__(self, rate_per_minutes: Dict[BikeType]) -> None:
        self._rate = rate_per_minutes

    def calculate_fee(self, trip: Trip, end_time: int) -> float:
        return _minutes(trip=trip, end_time=end_time) * 

class TiredPricing(PricingStrategy):

    def __int__(
            self, 
            clock : Clock,
            first_hour_rates: dict = {}, 
            next_hour_rates: dict = {},    
        ):
        self._first_hour = first_hour_rates
        self._next_hour = next_hour_rates
        self._clock = clock

    def calculate_fee(self, trip: Trip) -> float:
        if trip._start_time < self._clock.now():
            raise ValueError("invalid start time of trip")
        start_time = trip._start_time
        exit_time = self._clock.now()

        total_hours = math.Max(1.0, (exit_time - start_time) / 60)
        fee = self._first_hour[trip.bike_type]
        if total_hours > 1:
            fee += (total_hours - 1) * self._next_hour[trip.bike_type]

        return fee
    


class BikeStationService:

    def __int__(
        self,
        stations : list, # list[Stations]
        clock : Clock,
        station_selection_svc: StationSelectionStrategy,
        pricing_svc: PricingStrategy,
    ):
        self.stations = stations
        self._booked_list: dict = {}
        self._lock = threading.Lock()
        self._cnt = count(1)
        self._clock = clock
        self._station_selection_svc = station_selection_svc
        self._pricing_svc = pricing_svc

    # user went to a particular location book picking the bike
    def book_bike(
            self, 
            stataion: Station,
            bike_type : Optional[BikeType] = None
        ) -> Optional[Trip]: #Ticket
        with self._lock:
            if bike_type:
                for dock in stataion.dock_list:
                    if dock.is_bike_free(bike_type=bike_type):
                        trip = Trip(
                            trip_id=f"trip-{next(self._cnt)}",
                            bike_type=bike_type,
                            start_station=stataion,
                            start_time=self._clock.now()
                        )

                        bike = Bike(
                            bike_id=f"bike-{next(self._cnt)}"
                            bike_type=bike_type
                        )
                        
                        dock.occupy()
                        # kind of db save (in-memory for now)
                        self._booked_list[trip.trip_id] = trip

                        return trip

                raise ValueError(f"bike not available at this stations of type {bike_type}")
            else:
                # book any avalable bike the the given station
                for doc in stataion.dock_list:
                    if doc.is_dock_free():
                        trip = Trip(
                            trip_id=f"trip-{next(self._cnt)}",
                            bike_type=bike_type,
                            start_station=stataion,
                            start_time=self._clock.now()
                        )
                        
                        bike = Bike(
                            bike_id=f"bike-{next(self._cnt)}"
                            bike_type=bike_type
                        )

                        dock.occupy()
                        self._booked_list[trip.trip_id] = trip

                        return trip
                    
        return None

    def drop_bike(self, trip: Trip '''Ticket''') -> float: #fee
        # find the nearest available station
        with self._lock:
            station = self._station_selection_svc.find_station(bike=bike)
            if not station:
                raise ValueError(f"No doc availabe at the nearest station")
            
            trip = self._booked_list[trip.trip_id]
            if not trip:
                raise ValueError("Invaid trip")
            
            trip._drop_time = self._clock.now()
            trip._fee = self._pricing_svc.calculate_fee(trip=trip)

            del self._booked_list[trip.trip_id]

    

def main():
    pass



        
