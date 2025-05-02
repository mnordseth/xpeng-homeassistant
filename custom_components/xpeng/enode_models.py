from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


@dataclass
class Information:
    display_name: Optional[str]
    vin: str
    brand: str
    model: str
    year: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Information":
        return cls(
            display_name=data["displayName"],
            vin=data["vin"],
            brand=data["brand"],
            model=data["model"],
            year=data["year"],
        )


@dataclass
class ChargeState:
    charge_rate: Optional[float]
    charge_time_remaining: Optional[int]
    is_fully_charged: bool
    is_plugged_in: bool
    is_charging: bool
    battery_level: int
    range: int
    battery_capacity: float
    charge_limit: int
    last_updated: Optional[datetime]
    power_delivery_state: str
    max_current: Optional[int]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "ChargeState":
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
    deadline: Optional[datetime]
    is_enabled: bool
    minimum_charge_limit: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "SmartChargingPolicy":
        return cls(
            deadline=parse_datetime(data["deadline"]),
            is_enabled=data["isEnabled"],
            minimum_charge_limit=data["minimumChargeLimit"],
        )


@dataclass
class Location:
    id: Optional[str]
    latitude: float
    longitude: float
    last_updated: Optional[datetime]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Location":
        return cls(
            id=data["id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            last_updated=parse_datetime(data["lastUpdated"]),
        )


@dataclass
class Odometer:
    distance: Optional[float]
    last_updated: Optional[datetime]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Odometer":
        return cls(
            distance=data["distance"],
            last_updated=parse_datetime(data["lastUpdated"]),
        )


@dataclass
class Capability:
    intervention_ids: List[str]
    is_capable: bool

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Capability":
        return cls(
            intervention_ids=data.get("interventionIds", []),
            is_capable=data.get("isCapable", False),
        )


@dataclass
class Capabilities:
    information: Capability
    charge_state: Capability
    location: Capability
    odometer: Capability
    set_max_current: Capability
    start_charging: Capability
    stop_charging: Capability
    smart_charging: Capability

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Capabilities":
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
    id: str
    user_id: str
    vendor: str
    is_reachable: bool
    last_seen: Optional[datetime]
    information: Information
    charge_state: ChargeState
    smart_charging_policy: SmartChargingPolicy
    location: Location
    odometer: Odometer
    capabilities: Capabilities
    scopes: List[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Vehicle":
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
    after: Optional[str]
    before: Optional[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Pagination":
        return cls(
            after=data["after"],
            before=data["before"],
        )


@dataclass
class EnodeResponse:
    data: List[Vehicle]
    pagination: Pagination

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "EnodeResponse":
        vehicles = [
            Vehicle.from_json(vehicle_data) for vehicle_data in json_data["data"]
        ]
        pagination = Pagination.from_json(json_data["pagination"])
        return cls(data=vehicles, pagination=pagination)
