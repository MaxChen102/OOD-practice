from vehicle import VehicleSize


class ParkingSpot:
    def __init__(self, spot_id: str, size: VehicleSize) -> None:
        self.spot_id = spot_id
        self.size = size
        self._occupied = False

    def can_fit(self, size: VehicleSize) -> bool:
        return self.size.value >= size.value

    def is_available(self) -> bool:
        return not self._occupied

    def park(self) -> None:
        if self._occupied:
            raise ValueError(f"Spot {self.spot_id} is already occupied")
        self._occupied = True

    def vacate(self) -> None:
        if not self._occupied:
            raise ValueError(f"Spot {self.spot_id} is already empty")
        self._occupied = False
