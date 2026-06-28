"""
Problem 01: Parking Lot System
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Allowed: Python stdlib only (enum, abc, dataclasses, datetime, typing, threading, itertools).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import math
import time, threading
from itertools import count

class VehicleType(str, Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    BICYCLE = "bicycle"

class SpotType(str, Enum):
    COMPACT = "compact"
    LARGE = "large"
    MOTORCYCLE = "motorcycle"
    BICYCLE = "bicycle"

    def accept(self, vehicle_type: VehicleType) -> bool:
        return vehicle_type in _SPOT_FITS[self]
            
_SPOT_FITS = {
    SpotType.MOTORCYCLE : {VehicleType.MOTORCYCLE},
    SpotType.COMPACT : {VehicleType.CAR, VehicleType.MOTORCYCLE},
    SpotType.LARGE : { VehicleType.TRUCK, VehicleType.CAR, VehicleType.MOTORCYCLE}, 
    SpotType.BICYCLE : { VehicleType.BICYCLE }
}
_SPOT_SIZE = {SpotType.MOTORCYCLE: 0, SpotType.COMPACT: 1, SpotType.LARGE: 2}
        
class Vehicle:
    def __init__(self, vehicle_type: VehicleType, vehicle_number:str):
        self.vehicle_type = vehicle_type
        self.vehicle_number = vehicle_number

class ParkingSpot:
    def __init__(
            self, 
            spot_id : str,
            spot_type: SpotType, 
            floor_number:int,
        ):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.floor_number = floor_number
        self._is_occupied = False

    @property
    def is_occupied(self) -> bool:
        return self._is_occupied
    
    def occupy(self) -> None:
        if self._is_occupied:
            raise ValueError(f"spot {self.spot_id} already occupied")

        self._is_occupied = True

    def vacate(self) -> None:
        if not self._is_occupied:
            raise ValueError(f"spot {self.spot_id} already empty")
        self._is_occupied = False

class ParkingFloor:
    CAPACITY_LIMIT = {
        1 : 100,
        2 : 50,
        3 : 25
    }

    def __init__(
            self, 
            floor_number:int, 
            parking_spots: list = None
        ):

        self.floor_number = floor_number
        self.parking_spots = parking_spots if parking_spots is not None else []

    @property
    def floor_number(self):
        return self._floor_number
    
    @floor_number.setter
    def floor_number(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("floor must be an integer")
        
        if value not in self.CAPACITY_LIMIT:
            raise ValueError(f"Invalid floor {value}. Only floors 1, 2, and 3 are available.")
        self._floor_number = value

    @property
    def parking_spots(self):
        return self._parking_spots

    @parking_spots.setter
    def parking_spots(self, value : list):
        if not isinstance(value, list):
            raise ValueError("parking spots must have to be a list")
        
        max_limit = self.CAPACITY_LIMIT[self.floor_number]
        if len(value) > max_limit : 
            raise ValueError(f"floor {self.floor_number} exceeded it's limit"
                             f"max allowed floors are {max_limit} assing the lower vlaue")
        
        self._parking_spots = value

class Ticket:
    def __init__(
            self, 
            ticket_number : str,
            vehicle : Vehicle,
            parking_spot : ParkingSpot,
            entry_time : int,
    ):
        self.ticket_number = ticket_number
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_time = entry_time
        self.exit_time = None
        self.fee = None

    
    def __str__(self):
        return (
           f"Ticket(ticket_number={self.ticket_number},"
           f"Vehicle(vehicle_number={self.vehicle.vehicle_number}, vehicle_type={self.vehicle.vehicle_type})"
           f"ParkingSpot(spot_id={self.parking_spot.spot_id}, spot_type={self.parking_spot.spot_type}, floor_number={self.parking_spot.floor_number}))"
           )

    

class SpotAssignmentStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: list[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
       ...


class NearestAssingmentStrategy(SpotAssignmentStrategy):

    def find_spot(self, floors: list[ParkingFloor], vehicle : Vehicle) -> Optional[ParkingSpot]:
        for floor in floors:
            for spot in floor.parking_spots:
                if not spot.is_occupied and spot.spot_type.accept(vehicle.vehicle_type):
                    return spot
                
        return None

class BestFirtAssignmentStrategy(SpotAssignmentStrategy):

    def find_spot(self, floors: list[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        best = None
        for floor in floors:
            for spot in floor.parking_spots:
                if spot.is_occupied or not spot.spot_type.accept(vehicle.vehicle_type):
                    continue

                if best is None and _SPOT_SIZE[spot.spot_type] < _SPOT_SIZE[spot.spot_type]:
                    best = best
        
        return best
    

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket, exit_time: int) -> float:
        ...

class FlatPerHourPricing(PricingStrategy):

    def __init__(self, rate_per_hour: dict):
        self._rate = rate_per_hour

    def calculate_fee(self, ticket: Ticket, exit_time: int) -> float:
        if exit_time < ticket.entry_time:
            raise ValueError("exit time can't be before entry time")

        total_time = exit_time - ticket.entry_time
        hours = max(1, math.ceil(total_time / 60))

        return hours * self._rate[ticket.vehicle.vehicle_type]
    
class TiredPricing(PricingStrategy):

    def __init__(self, first_hour_pricing: dict, extra_hour_pricing: dict):
        self._first_hour = first_hour_pricing
        self._extra_hour = extra_hour_pricing

    def calculate_fee(self, ticket, exit_time) -> float:
        if exit_time < ticket.entry_time:
            raise ValueError("exit time can't be before entry time")
        
        total_minutes = exit_time = ticket.entry_time
        hours = max(1, math.ceil(total_minutes / 60))

        charges = self._first_hour[ticket.vehicle.vehicle_type]
        if hours > 1:
            charges += (hours - 1) * self._extra_hour[ticket.vehicle.vehicle_type]
        
        return charges

class Clock(ABC):

    @abstractmethod
    def now(self) -> int:
        ...

class FakeClock(Clock):
    def __init__(self, start_time: int = 0):
        self._t = start_time

    def now(self) -> int:
        return self._t
    
    def advance(self, minutes: int) :
        self._t = self._t + minutes

class ParkingLot:
    def __init__(
            self, 
            floors : list,
            assignement_svc: SpotAssignmentStrategy,
            pricing_svc: PricingStrategy,
            clock : Clock,

        ) -> None:

        self.floors = floors
        self.assignment_svc = assignement_svc
        self.pricing_svc = pricing_svc
        self._clock  = clock
        self._active_tickets: dict = {}
        self._lock = threading.Lock()
        self._ticket_seq = count(1)


    def park(self, vehicle: Vehicle) -> Ticket:
        with self._lock :
            spot = self.assignment_svc.find_spot(floors=self.floors, vehicle=vehicle)
            if not spot:
                return None
            spot.occupy()
            
            # create ticket
            ticket = Ticket(
                ticket_number=f"t-{next(self._ticket_seq)}",
                vehicle=vehicle,
                parking_spot=spot,
                entry_time=self._clock.now()
            )

            self._active_tickets[ticket.ticket_number] = ticket
            # self._ticket_seq ++ , next automatically increases the counter 
            return ticket

    def unpark(self, ticket: Ticket) -> float:
        with self._lock:
            ticket = self._active_tickets.get(ticket.ticket_number)
            if not ticket:
                raise ValueError(" known ticket number ")
            
            exit_time = self._clock.now()
            fee = self.pricing_svc.calculate_fee(ticket=ticket, exit_time=exit_time)
            ticket.exit_time = exit_time
            ticket.fee = fee

            ticket.parking_spot.vacate()
            del self._active_tickets[ticket.ticket_number]
        
        return fee
    
    def available_count(self) -> int:
        return sum(1 for f in self.floors
                for s in f.parking_spots if not s.is_occupied)

    def available_spot(self) -> dict:
        count_by_floors = {f.floor_number : sum(1 for s in f.parking_spots if not s.is_occupied)
                  for f in self.floors}
        return count_by_floors


def build_floors():

    return [
       ParkingFloor(
           floor_number=1,
           parking_spots=[ParkingSpot(
               spot_id="BK-0",
               spot_type=SpotType.MOTORCYCLE,
               floor_number=1,
           ), ParkingSpot(
               spot_id="CP-1",
               spot_type=SpotType.COMPACT,
               floor_number=1,
           ), ParkingSpot(
               spot_id="TR-2",
               spot_type=SpotType.LARGE,
               floor_number=1
           ), ParkingSpot(
               spot_id="BC-3",
               spot_type=SpotType.BICYCLE,
               floor_number=1
           )]
       ),
       ParkingFloor(
           floor_number=2,
           parking_spots=[ParkingSpot(
               spot_id="BK-1",
               spot_type=SpotType.MOTORCYCLE,
               floor_number=2,
           ), ParkingSpot(
                spot_id="CP-2",
                spot_type=SpotType.COMPACT,
                floor_number=2,
           ), ParkingSpot(
                spot_id="TR-3",
                spot_type=SpotType.LARGE,
                floor_number=2
           ), ParkingSpot(
                spot_id="BC-4",
                spot_type=SpotType.BICYCLE,
                floor_number=1
           )]
       ),
    ]


def main() -> None:
    clock = FakeClock(start_time=0)
    parking_lot = ParkingLot(
        floors=build_floors(),
        assignement_svc=NearestAssingmentStrategy(),
        pricing_svc=FlatPerHourPricing(rate_per_hour=20),
        clock=clock,
    )


    ticket = parking_lot.park(Vehicle(VehicleType.CAR, "VECH-23"))
    print(parking_lot.available_spot())
    print(ticket)
    bicycle_ticket = parking_lot.park(Vehicle(VehicleType.BICYCLE, "VECH-24"))
    print(parking_lot.available_spot())
    print(bicycle_ticket)


if __name__ == "__main__":
    main()
