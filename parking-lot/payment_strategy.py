from abc import ABC, abstractmethod

from parking_ticket import ParkingTicket
from vehicle import VehicleType


class PaymentStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: ParkingTicket) -> float:
        ...


class FlatFeeStrategy(PaymentStrategy):
    def __init__(self, rate_per_hour: float) -> None:
        self.rate_per_hour = rate_per_hour

    def calculate_fee(self, ticket: ParkingTicket) -> float:
        return self.rate_per_hour * ticket.duration_hours


class VehicleBasedFeeStrategy(PaymentStrategy):
    def __init__(self, rates: dict[VehicleType, float]) -> None:
        self.rates = rates

    def calculate_fee(self, ticket: ParkingTicket) -> float:
        rate = self.rates[ticket.vehicle_type]
        return rate * ticket.duration_hours
