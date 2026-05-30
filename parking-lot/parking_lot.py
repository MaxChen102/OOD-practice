from datetime import datetime

from parking_floor import ParkingFloor
from parking_strategy import ParkingStrategy
from parking_ticket import ParkingTicket
from payment_strategy import PaymentStrategy
from vehicle import Vehicle, VehicleType


class ParkingLot:
    def __init__(
        self,
        floors: list[ParkingFloor],
        parking_strategy: ParkingStrategy,
        payment_strategy: PaymentStrategy,
    ) -> None:
        self.floors = floors
        self.parking_strategy = parking_strategy
        self.payment_strategy = payment_strategy
        self._active_tickets: dict[str, ParkingTicket] = {}
        self._ticket_counter = 0

    def _next_ticket_id(self) -> str:
        self._ticket_counter += 1
        return f"T{self._ticket_counter:06d}"

    def park_vehicle(self, vehicle: Vehicle, entry_time: datetime | None = None) -> ParkingTicket | None:
        when = entry_time or datetime.now()
        for floor in self.floors:
            spot = floor.find_spot(vehicle, self.parking_strategy)
            if spot is None:
                continue
            spot.park()
            ticket = ParkingTicket(
                self._next_ticket_id(),
                vehicle,
                floor.level,
                spot,
                when,
            )
            self._active_tickets[vehicle.license_plate] = ticket
            return ticket
        return None

    def unpark_vehicle(self, license_plate: str, exit_time: datetime | None = None) -> float:
        when = exit_time or datetime.now()
        ticket = self._active_tickets.pop(license_plate, None)
        if ticket is None:
            raise ValueError(f"No active ticket for {license_plate}")
        ticket.close(when)
        ticket.spot.vacate()
        return self.payment_strategy.calculate_fee(ticket)

    def availability(self, vehicle_type: VehicleType | None = None) -> dict[int, int]:
        return {floor.level: floor.available_count(vehicle_type) for floor in self.floors}

    def is_full(self, vehicle_type: VehicleType) -> bool:
        return sum(self.availability(vehicle_type).values()) == 0
