"""Sensor platform for xpeng."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.const import (
    PERCENTAGE,
    #    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    #    UnitOfPressure,
    #    UnitOfSpeed,
    #    UnitOfTemperature,
    #    UnitOfTime,
)
from homeassistant.helpers.icon import icon_for_battery_level


from .entity import XpengEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from .data import XpengConfigEntry
    from .coordinator import XpengDataUpdateCoordinator

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: XpengConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entities = []
    for vehicle_id, vehicle in enumerate(entry.runtime_data.client.vehicles):
        _LOGGER.debug("Setting up sensor for %s", vehicle)
        entities.append(XpengCarBattery(vehicle_id, entry.runtime_data.coordinator))
        entities.append(
            XpengCarBatteryTarget(vehicle_id, entry.runtime_data.coordinator)
        )
        entities.append(XpengCarRange(vehicle_id, entry.runtime_data.coordinator))
        entities.append(XpengCarChargeRate(vehicle_id, entry.runtime_data.coordinator))

    async_add_entities(entities, update_before_add=True)


class XpengCarBattery(XpengEntity, SensorEntity):
    """Representation of the Xpeng car battery sensor."""

    entity_name = "battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:battery"

    def __init__(
        self, vehicle_id: int, coordinator: XpengDataUpdateCoordinator
    ) -> None:
        """Create Xpeng Car Battery sensor entity."""
        super().__init__(vehicle_id, coordinator)
        _LOGGER.debug(
            "Create XpengCarBattery: '%s' Device '%s'", self.name, self.device_info
        )

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return battery level."""
        # usable_battery_level matches the Xpeng app and car display
        return self.coordinator.data[self._vehicle_id].charge_state.battery_level

    @property
    def icon(self):
        """Return icon for the battery."""
        charging = self.coordinator.data[self._vehicle_id].charge_state.is_charging

        return icon_for_battery_level(
            battery_level=self.native_value, charging=charging
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "raw_soc": self.coordinator.data[
                self._vehicle_id
            ].charge_state.battery_level,
        }


class XpengCarBatteryTarget(XpengEntity, SensorEntity):
    """Representation of the Xpeng car battery target charge level."""

    entity_name = "battery target"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:battery"

    def __init__(
        self, vehicle_id: int, coordinator: XpengDataUpdateCoordinator
    ) -> None:
        """Create sensor entity for Xpeng battery target charge level."""
        super().__init__(vehicle_id, coordinator)
        _LOGGER.debug(
            "Create XpengCarBatteryTarget: '%s' Device '%s'",
            self.name,
            self.device_info,
        )

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return battery level."""
        # usable_battery_level matches the Xpeng app and car display
        return self.coordinator.data[self._vehicle_id].charge_state.charge_limit

    @property
    def icon(self):
        """Return icon for the battery."""
        return icon_for_battery_level(battery_level=self.native_value)


class XpengCarRange(XpengEntity, SensorEntity):
    """Representation of the Xpeng car range sensor."""

    entity_name = "range"
    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS
    _attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> float:
        """Return range."""
        return self.coordinator.data[self._vehicle_id].charge_state.range


class XpengCarChargeRate(XpengEntity, SensorEntity):
    """Representation of the Xpeng car charging rate."""

    entity_name = "charge rate"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_icon = "mdi:flash"

    @property
    def native_value(self) -> float:
        """Return range."""
        return self.coordinator.data[self._vehicle_id].charge_state.charge_rate or 0
