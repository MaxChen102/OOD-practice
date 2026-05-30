from abc import ABC, abstractmethod

from parking_spot import ParkingSpot
from vehicle import Vehicle


class ParkingStrategy(ABC):
    @abstractmethod
    def choose_spot(self, candidates: list[ParkingSpot], vehicle: Vehicle) -> ParkingSpot | None:
        ...


class NearestFirstStrategy(ParkingStrategy):
    def choose_spot(self, candidates: list[ParkingSpot], vehicle: Vehicle) -> ParkingSpot | None:
        return candidates[0] if candidates else None


class FurthestFirstStrategy(ParkingStrategy):
    def choose_spot(self, candidates: list[ParkingSpot], vehicle: Vehicle) -> ParkingSpot | None:
        return candidates[-1] if candidates else None


class BestFitStrategy(ParkingStrategy):
    def choose_spot(self, candidates: list[ParkingSpot], vehicle: Vehicle) -> ParkingSpot | None:
        fitting = [s for s in candidates if s.size.value >= vehicle.size.value]
        if not fitting:
            return None
        return min(fitting, key=lambda s: s.size.value)
