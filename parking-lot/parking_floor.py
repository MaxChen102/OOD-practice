from parking_spot import ParkingSpot
from parking_strategy import ParkingStrategy
from vehicle import Vehicle, VehicleSize, VehicleType


class ParkingFloor:
    def __init__(self, level: int, rows: int, cols: int, spot_layout: list[list[VehicleSize]]) -> None:
        self.level = level
        self._spots: list[list[ParkingSpot]] = []
        for row in range(rows):
            row_spots: list[ParkingSpot] = []
            for col in range(cols):
                size = spot_layout[row][col]
                spot_id = f"L{level}-R{row}-C{col}"
                row_spots.append(ParkingSpot(spot_id, size))
            self._spots.append(row_spots)

    def all_spots(self) -> list[ParkingSpot]:
        return [spot for row in self._spots for spot in row]

    def find_spot(self, vehicle: Vehicle, strategy: ParkingStrategy) -> ParkingSpot | None:
        candidates = [
            spot
            for spot in self.all_spots()
            if spot.is_available() and spot.can_fit(vehicle.size)
        ]
        return strategy.choose_spot(candidates, vehicle)

    def available_count(self, vehicle_type: VehicleType | None = None) -> int:
        spots = self.all_spots()
        if vehicle_type is None:
            return sum(1 for s in spots if s.is_available())
        return sum(
            1 for s in spots if s.is_available() and s.can_fit(Vehicle.default_size(vehicle_type))
        )
