import unittest
from datetime import datetime, timedelta

from parking_floor import ParkingFloor
from parking_lot import ParkingLot
from parking_strategy import NearestFirstStrategy
from payment_strategy import FlatFeeStrategy
from vehicle import Vehicle, VehicleSize, VehicleType


def new_lot(spot_layout: list[list[VehicleSize]]) -> ParkingLot:
    rows = len(spot_layout)
    cols = len(spot_layout[0]) if spot_layout else 0
    floor = ParkingFloor(level=0, rows=rows, cols=cols, spot_layout=spot_layout)
    return ParkingLot(
        floors=[floor],
        parking_strategy=NearestFirstStrategy(),
        payment_strategy=FlatFeeStrategy(rate_per_hour=10.0),
    )


def single_spot_lot(size: VehicleSize) -> ParkingLot:
    return new_lot([[size]])


def total_available(lot: ParkingLot) -> int:
    return sum(lot.availability().values())


class TestParkingLot(unittest.TestCase):
    def test_initialize_all_spots_empty(self) -> None:
        lot = new_lot([
            [VehicleSize.SMALL, VehicleSize.MEDIUM, VehicleSize.LARGE],
        ])
        floor = lot.floors[0]

        self.assertEqual(total_available(lot), 3)
        self.assertTrue(all(spot.is_available() for spot in floor.all_spots()))

    def test_park_car_decreases_available_spots_by_one(self) -> None:
        lot = new_lot([[VehicleSize.MEDIUM]])
        initial = total_available(lot)

        ticket = lot.park_vehicle(Vehicle("CAR-1", VehicleType.CAR))

        self.assertIsNotNone(ticket)
        self.assertEqual(total_available(lot), initial - 1)
        self.assertEqual(lot.availability(VehicleType.CAR)[0], 0)

    def test_park_car_then_exit_returns_to_full(self) -> None:
        lot = new_lot([[VehicleSize.MEDIUM]])
        initial = total_available(lot)
        entry = datetime(2025, 1, 1, 10, 0)
        exit_ = entry + timedelta(hours=1)

        lot.park_vehicle(Vehicle("CAR-1", VehicleType.CAR), entry_time=entry)
        self.assertEqual(total_available(lot), initial - 1)

        lot.unpark_vehicle("CAR-1", exit_time=exit_)
        self.assertEqual(total_available(lot), initial)
        self.assertEqual(lot.availability(VehicleType.CAR)[0], 1)

    def test_park_truck_in_car_spot_fails(self) -> None:
        lot = single_spot_lot(VehicleSize.MEDIUM)
        ticket = lot.park_vehicle(Vehicle("TRUCK-1", VehicleType.TRUCK))
        self.assertIsNone(ticket)
        self.assertEqual(total_available(lot), 1)

    def test_park_truck_in_bike_spot_fails(self) -> None:
        lot = single_spot_lot(VehicleSize.SMALL)
        ticket = lot.park_vehicle(Vehicle("TRUCK-1", VehicleType.TRUCK))
        self.assertIsNone(ticket)
        self.assertEqual(total_available(lot), 1)

    def test_park_car_in_bike_spot_fails(self) -> None:
        lot = single_spot_lot(VehicleSize.SMALL)
        ticket = lot.park_vehicle(Vehicle("CAR-1", VehicleType.CAR))
        self.assertIsNone(ticket)
        self.assertEqual(total_available(lot), 1)

    def test_park_car_in_truck_spot_passes(self) -> None:
        lot = single_spot_lot(VehicleSize.LARGE)
        ticket = lot.park_vehicle(Vehicle("CAR-1", VehicleType.CAR))
        self.assertIsNotNone(ticket)
        assert ticket is not None
        self.assertEqual(ticket.spot.size, VehicleSize.LARGE)
        self.assertFalse(ticket.spot.is_available())
        self.assertEqual(total_available(lot), 0)

    def test_park_bike_in_car_spot_passes(self) -> None:
        lot = single_spot_lot(VehicleSize.MEDIUM)
        ticket = lot.park_vehicle(Vehicle("BIKE-1", VehicleType.MOTORCYCLE))
        self.assertIsNotNone(ticket)
        assert ticket is not None
        self.assertEqual(ticket.spot.size, VehicleSize.MEDIUM)
        self.assertFalse(ticket.spot.is_available())
        self.assertEqual(total_available(lot), 0)

    def test_park_bike_in_truck_spot_passes(self) -> None:
        lot = single_spot_lot(VehicleSize.LARGE)
        ticket = lot.park_vehicle(Vehicle("BIKE-1", VehicleType.MOTORCYCLE))
        self.assertIsNotNone(ticket)
        assert ticket is not None
        self.assertEqual(ticket.spot.size, VehicleSize.LARGE)
        self.assertFalse(ticket.spot.is_available())
        self.assertEqual(total_available(lot), 0)


if __name__ == "__main__":
    unittest.main()
