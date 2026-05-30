from enum import Enum


class VehicleType(Enum):
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    TRUCK = "truck"


class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Vehicle:
    _DEFAULT_SIZES: dict[VehicleType, VehicleSize] = {
        VehicleType.MOTORCYCLE: VehicleSize.SMALL,
        VehicleType.CAR: VehicleSize.MEDIUM,
        VehicleType.TRUCK: VehicleSize.LARGE,
    }

    def __init__(
        self,
        license_plate: str,
        vehicle_type: VehicleType,
        size: VehicleSize | None = None,
    ) -> None:
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.size = size if size is not None else self._DEFAULT_SIZES[vehicle_type]

    @classmethod
    def default_size(cls, vehicle_type: VehicleType) -> VehicleSize:
        return cls._DEFAULT_SIZES[vehicle_type]
