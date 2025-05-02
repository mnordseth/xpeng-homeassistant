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
    from .enode_models import Vehicle
    from .coordinator import XpengDataUpdateCoordinator
    from .data import XpengConfigEntry

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .coordinator import XpengDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: XpengConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entities = []
    for vehicle in entry.runtime_data.client.vehicles:
        _LOGGER.debug("Setting up device tracker for %s", vehicle)
        entities.append(XpengCarLocation(vehicle, entry.runtime_data.coordinator))

    async_add_entities(entities, update_before_add=True)


class XpengCarLocation(XpengEntity, TrackerEntity):
    """Representation of a Xpeng car location device tracker."""

    entity_name = "location tracker"

    def __init__(
        self, vehicle: Vehicle, coordinator: XpengDataUpdateCoordinator
    ) -> None:
        """Create device tracker for Xpeng vehicle."""
        super().__init__(vehicle, coordinator)

    @property
    def source_type(self):
        """Return device tracker source type."""
        return const.ATTR_GPS

    @property
    def longitude(self):
        """Return longitude."""
        return self._vehicle.location.longitude

    @property
    def latitude(self):
        """Return latitude."""
        return self._vehicle.location.latitude

    #    @property
    #    def extra_state_attributes(self):
    #        """Return device state attributes."""
    ##        return {
    #           "heading": self._car.heading,
    #           "speed": self._car.speed,
    #       }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
