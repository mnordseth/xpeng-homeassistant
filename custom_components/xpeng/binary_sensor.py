"""Xpeng binary sensors."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .entity import XpengEntity
from .data import XpengConfigEntry

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
        entities.append(XpengCarCharging(vehicle_id, entry.runtime_data.coordinator))
        entities.append(XpengCarPluggedIn(vehicle_id, entry.runtime_data.coordinator))

    async_add_entities(entities, update_before_add=True)


class XpengCarCharging(XpengEntity, BinarySensorEntity):
    """Representation of Xpeng car charging binary sensor."""

    entity_name = "charging"
    _attr_icon = "mdi:ev-station"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        # _LOGGER.debug(
        #    "XpengCarCharging.is_on(): %s Coordinator data: %s",
        #    self._vehicle.charge_state.is_charging,
        #    self.coordinator.data,
        # )
        return self.coordinator.data[self._vehicle_id].charge_state.is_charging
        # return self._vehicle.charge_state.is_charging


class XpengCarPluggedIn(XpengEntity, BinarySensorEntity):
    """Representation of Xpeng car charging binary sensor."""

    entity_name = "plugged in"
    _attr_icon = "mdi:ev-station"
    _attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        return self.coordinator.data[self._vehicle_id].charge_state.is_plugged_in
