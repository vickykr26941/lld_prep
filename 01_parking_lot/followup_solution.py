


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
from typing import Optional, List, Tuple, Dict,Callable



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
    def select(
        self, 
        stations: List[Station], 
        origin: Tuple[float, float], 
        is_eligible: Callable[[Station], bool]
    ) -> Optional[Station]:
        ...

class NearestSelectionStrategy(StationSelectionStrategy):
    def select(self, stations, origin, is_eligible) -> Optional[Station]:
        best : Optional[Station] = None
        best_dist = math.inf
        for station in stations:
            if not is_eligible(station):
                continue
            d = self._dist(origin, station.location)
            if d < best_dist:
                best = station
                best_dist = d
        
        return best

    def _dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return (a[0] - b[0]) ** 2 +  (a[1] - b[1]) ** 2
    
    

def _minutes(trip: Trip, end_time: int) -> int:
    return end_time - trip.start_time

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, trip: Trip, end_time: int) -> float:
        ...

class FlatPerMinutePricing(PricingStrategy):
    def __init__(self, rate_per_minutes: Dict[BikeType]) -> None:
        self._rate = rate_per_minutes

    def calculate_fee(self, trip: Trip, end_time: int) -> float:
        return _minutes(trip=trip, end_time=end_time) * self._rate[trip.bike.bike_type]
    
class TiredPricing(PricingStrategy):

    def __int__(
            self, 
            free_minutes: int,
            rate_per_minutes: Dict[BikeType]
        ):
        self._free = free_minutes
        self._rate = rate_per_minutes

    def calculate_fee(self, trip: Trip, end_time: int) -> float:
        if end_time < trip.start_time:
            raise ValueError("invalid end time")
        
        billable = max(0, _minutes(trip=trip, end_time=end_time) - self._free)
        return billable * self._rate[trip.bike.bike_type]


class BikeShareService:

    def __int__(
        self,
        stations : list, # list[Stations]
        clock : Clock,
        station_selection_svc: StationSelectionStrategy,
        pricing_svc: PricingStrategy,
    ):
        self.stations = stations
        self._clock = clock
        self._station_selection_svc = station_selection_svc
        self._pricing_svc = pricing_svc

        self._active: Dict = {}
        self._trip_seq: int = count(1)
        self._lock = threading.Lock()

    
    def rent_bike(self, station:Station, bike_type: BikeType) -> Optional[Trip]:
        with self._lock:
            if not station.has_bike(bike_type=bike_type):
                raise ValueError(f"Station {station.station_name} has no free bike")
            
            dock = station.find_dock_with_bike(bike_type=bike_type)
            bike = dock.release_bike()

            trip = Trip(
                trip_id=f"trip-f{next(self._trip_seq)}",
                bike=bike,
                start_station=station,
                start_time=self._clock.now()
            )

            self._active[trip.trip_id] = trip

            return trip

    def rent_bike(
            self, 
            station:Station, 
            origin: Tuple[float, float],
        ) -> Optional[Trip]:
        with self._lock:
            if not station.has_free_dock():
                raise ValueError(f"Station {station.station_name} has not free dock")
            
            dock = station.find_free_dock()
            bike = dock.release_bike()

            trip = Trip(
                trip_id=f"trip-{next(self._trip_seq)}",
                bike=bike,
                start_station=station,
                start_time=self._clock.now()
            )

            self._active[trip.trip_id] = trip
            return trip
    
    # rent bike find the nearest pickup station only provided the user location
    def rent_bike():
        pass

    def return_bike(self, trip: Trip, station:Station) -> float:
        with self._lock:
            if self._active.get(trip.trip_id) is None:
                raise ValueError("Invalid trip")
            
            fee = self._pricing_svc.calculate_fee(trip=trip, end_time=self._clock.now())
            trip.fee = fee
            trip.end_station = station
            trip.end_time = self._clock.now()

            dock = station.find_free_dock()
            if not dock:
                raise ValueError(f" No Dock free at this station")
            dock.doc_bike()

            del self._active[trip.trip_id]

            return fee
        
    # drop bike at nearest available station with free dock , only provided user location.
    def return_bike():
        pass

    def nearest_return_station(self, origin:Tuple[float, float]) -> Optional[Station]:
        return self._station_selection_svc.select(
            stations=self.stations,
            origin=origin,
            is_eligible= lambda s: s.has_free_dock()
        )

    def nearest_pickup_station(self, origin:Tuple[float, float], bike_type: Optional[BikeType])-> Optional[Station]:
        if bike_type:
            def bike_available(station: Station) -> bool:
                return station.has_bike(bike_type=bike_type)
            
            station = self._station_selection_svc.select(
                stations=self.stations, 
                origin=origin,
                is_eligible=bike_available
            )
        else:
            def bike_available(station: Station) -> bool:
                return station.has_free_dock()
            
            station = self._station_selection_svc.select(
                stations=self.stations,
                origin=origin,
                is_eligible=bike_available,

            )

        return station
    
def build_stations() -> List[Station]:
    a = Station("A", "Station-A", (0.0, 0.0), [
        Dock("A1", Bike("b1", BikeType.STANDARD)),
        Dock("A2", Bike("b2", BikeType.STANDARD)),
        Dock("A3"),                                    
    ])
    b = Station("B", "Station-B", (3.0, 4.0), [
        Dock("B1", Bike("b3", BikeType.ELECTRIC)),
        Dock("B2", Bike("b4", BikeType.CARGO)),
        Dock("B3"),                                    
    ])
    c = Station("C", "Station-C", (1.0, 1.0), [
        Dock("C1"), Dock("C2"),                        
        Dock("C3", Bike("b5", BikeType.STANDARD)),
    ])
    return [a, b, c]

def main():

    clock = FakeClock(start=0)
    stations = build_stations()
    by_id = {s.station_id: s for s in stations}

    service = BikeShareService(
        stations=stations,
        clock=clock,
        pricing=TiredPricing(
            free_minutes=10,
            rate_per_minute={BikeType.STANDARD: 200, BikeType.ELECTRIC: 500, BikeType.CARGO: 800},
        ),
        selection=NearestSelectionStrategy(),
    )

    print("Initial availability:")
    for name, info in service.system_availability().items():
        print(f"  {name}: {info}")

    t1 = service.rent_bike(by_id["A"], BikeType.STANDARD)
    t2 = service.rent_bike(by_id["B"], BikeType.ELECTRIC)
    print(f"\nRented:\n  {t1}\n  {t2}")

    t3 = service.rent_bike(by_id["A"], BikeType.CARGO)
    print(f"\nRent CARGO at A -> {t3}   (None = no compatible bike, handled gracefully)")

    clock.advance(22)                                   # 22-minute ride
    rider_pos = (1.0, 1.0)
    dest = service.nearest_return_station(rider_pos)
    print(f"\nNearest free-dock station from {rider_pos}: {dest.name}")
    fee = service.return_bike(t1, dest)
    print(f"Returned {t1.bike} at {dest.name} after 22m -> fare {fee} paise (₹{fee/100:.2f})")

    print("\nFinal availability:")

    for name, info in service.system_availability().items():
        print(f"  {name}: {info}")

