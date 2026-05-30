from datetime import datetime

from parking_spot import ParkingSpot
from vehicle import Vehicle, VehicleType


class ParkingTicket:
    def __init__(
        self,
        ticket_id: str,
        vehicle: Vehicle,
        floor_level: int,
        spot: ParkingSpot,
        entry_time: datetime,
    ) -> None:
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.floor_level = floor_level
        self.spot = spot
        self.vehicle_type: VehicleType = vehicle.vehicle_type
        self.entry_time = entry_time
        self.exit_time: datetime | None = None

    def close(self, exit_time: datetime) -> None:
        self.exit_time = exit_time

    @property
    def duration_hours(self) -> float:
        if self.exit_time is None:
            raise ValueError("Ticket is still open")
        delta = self.exit_time - self.entry_time
        return max(delta.total_seconds() / 3600.0, 0.0)
