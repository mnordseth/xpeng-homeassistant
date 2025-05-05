"""Models for the Xpeng Enode API response."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


def parse_datetime(dt_str: str | None) -> datetime | None:
    """Parse an ISO format datetime string to a datetime object."""
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


@dataclass
class Information:
    """Vehicle information data."""

    display_name: str | None
    vin: str
    brand: str
    model: str
    year: int

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Information":
        """Create an Information instance from JSON data."""
        return cls(
            display_name=data["displayName"],
            vin=data["vin"],
            brand=data["brand"],
            model=data["model"],
            year=data["year"],
        )


@dataclass
class ChargeState:
    """Vehicle charging state data."""

    charge_rate: float | None
    charge_time_remaining: int | None
    is_fully_charged: bool
    is_plugged_in: bool
    is_charging: bool
    battery_level: int
    range: int
    battery_capacity: float
    charge_limit: int
    last_updated: datetime | None
    power_delivery_state: str
    max_current: int | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "ChargeState":
        """Create a ChargeState instance from JSON data."""
        return cls(
            charge_rate=data["chargeRate"],
            charge_time_remaining=data["chargeTimeRemaining"],
            is_fully_charged=data["isFullyCharged"],
            is_plugged_in=data["isPluggedIn"],
            is_charging=data["isCharging"],
            battery_level=data["batteryLevel"],
            range=data["range"],
            battery_capacity=data["batteryCapacity"],
            charge_limit=data["chargeLimit"],
            last_updated=parse_datetime(data["lastUpdated"]),
            power_delivery_state=data["powerDeliveryState"],
            max_current=data["maxCurrent"],
        )


@dataclass
class SmartChargingPolicy:
    """Vehicle smart charging policy data."""

    deadline: datetime | None
    is_enabled: bool
    minimum_charge_limit: int

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "SmartChargingPolicy":
        """Create a SmartChargingPolicy instance from JSON data."""
        return cls(
            deadline=parse_datetime(data["deadline"]),
            is_enabled=data["isEnabled"],
            minimum_charge_limit=data["minimumChargeLimit"],
        )


@dataclass
class Location:
    """Vehicle location data."""

    id: str | None
    latitude: float
    longitude: float
    last_updated: datetime | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Location":
        """Create a Location instance from JSON data."""
        return cls(
            id=data["id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            last_updated=parse_datetime(data["lastUpdated"]),
        )


@dataclass
class Odometer:
    """Vehicle odometer data."""

    distance: float | None
    last_updated: datetime | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Odometer":
        """Create an Odometer instance from JSON data."""
        return cls(
            distance=data["distance"],
            last_updated=parse_datetime(data["lastUpdated"]),
        )


@dataclass
class Capability:
    """Vehicle capability data."""

    intervention_ids: list[str]
    is_capable: bool

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Capability":
        """Create a Capability instance from JSON data."""
        return cls(
            intervention_ids=data.get("interventionIds", []),
            is_capable=data.get("isCapable", False),
        )


@dataclass
class Capabilities:
    """Vehicle capabilities data."""

    information: Capability
    charge_state: Capability
    location: Capability
    odometer: Capability
    set_max_current: Capability
    start_charging: Capability
    stop_charging: Capability
    smart_charging: Capability

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Capabilities":
        """Create a Capabilities instance from JSON data."""
        return cls(
            information=Capability.from_json(data["information"]),
            charge_state=Capability.from_json(data["chargeState"]),
            location=Capability.from_json(data["location"]),
            odometer=Capability.from_json(data["odometer"]),
            set_max_current=Capability.from_json(data["setMaxCurrent"]),
            start_charging=Capability.from_json(data["startCharging"]),
            stop_charging=Capability.from_json(data["stopCharging"]),
            smart_charging=Capability.from_json(data["smartCharging"]),
        )


@dataclass
class Vehicle:
    """Vehicle data."""

    id: str
    user_id: str
    vendor: str
    is_reachable: bool
    last_seen: datetime | None
    information: Information
    charge_state: ChargeState
    smart_charging_policy: SmartChargingPolicy
    location: Location
    odometer: Odometer
    capabilities: Capabilities
    scopes: list[str]

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Vehicle":
        """Create a Vehicle instance from JSON data."""
        return cls(
            id=data["id"],
            user_id=data["userId"],
            vendor=data["vendor"],
            is_reachable=data["isReachable"],
            last_seen=parse_datetime(data["lastSeen"]),
            information=Information.from_json(data["information"]),
            charge_state=ChargeState.from_json(data["chargeState"]),
            smart_charging_policy=SmartChargingPolicy.from_json(
                data["smartChargingPolicy"]
            ),
            location=Location.from_json(data["location"]),
            odometer=Odometer.from_json(data["odometer"]),
            capabilities=Capabilities.from_json(data["capabilities"]),
            scopes=data["scopes"],
        )


@dataclass
class Pagination:
    """Pagination data for API responses."""

    after: str | None
    before: str | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Pagination":
        """Create a Pagination instance from JSON data."""
        return cls(
            after=data["after"],
            before=data["before"],
        )


@dataclass
class EnodeResponse:
    """Complete Enode API response data."""

    data: list[Vehicle]
    pagination: Pagination

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> "EnodeResponse":
        """Create an EnodeResponse instance from JSON data."""
        vehicles = [
            Vehicle.from_json(vehicle_data) for vehicle_data in json_data["data"]
        ]
        pagination = Pagination.from_json(json_data["pagination"])
        return cls(data=vehicles, pagination=pagination)
