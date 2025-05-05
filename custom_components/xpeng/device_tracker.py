"""Support for Xpeng device tracker."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.device_tracker import const
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .entity import XpengEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
        _LOGGER.debug("Setting up device tracker for %s", vehicle)
        entities.append(XpengCarLocation(vehicle_id, entry.runtime_data.coordinator))

    async_add_entities(entities, update_before_add=True)


class XpengCarLocation(XpengEntity, TrackerEntity):
    """Representation of a Xpeng car location device tracker."""

    entity_name = "location tracker"

    @property
    def source_type(self) -> str:
        """Return device tracker source type."""
        return const.ATTR_GPS

    @property
    def longitude(self) -> float:
        """Return longitude."""
        return self.vehicle.location.longitude

    @property
    def latitude(self) -> float:
        """Return latitude."""
        return self.vehicle.location.latitude

    @property
    def force_update(self) -> bool:
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
