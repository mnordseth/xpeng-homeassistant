"""XpengEntity class."""

from __future__ import annotations
from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import XpengDataUpdateCoordinator

if TYPE_CHECKING:
    from .enode_models import Vehicle


class XpengEntity(CoordinatorEntity[XpengDataUpdateCoordinator]):
    """Base class for Xpeng entities."""

    entity_name = ""

    def __init__(
        self,
        vehicle_id: int,
        coordinator: XpengDataUpdateCoordinator,
    ) -> None:
        """Create base entity for Xpeng car data."""
        super().__init__(coordinator)

        self._vehicle_id = vehicle_id
        vehicle = coordinator.data[self._vehicle_id]
        display_name = f"{vehicle.information.brand} {vehicle.information.model}"
        self._attr_name = f"{display_name} {self.entity_name}"
        self._attr_unique_id = slugify(f"{vehicle.id} {self.entity_name}")
        self._attr_device_info = DeviceInfo(
            name=display_name,
            identifiers={(DOMAIN, vehicle.id)},
            manufacturer=vehicle.information.brand,
            model=vehicle.information.model,
            sw_version="",
            serial_number=vehicle.information.vin,
        )
        self._last_update_success: bool | None = None
        self.last_update_time: float | None = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
