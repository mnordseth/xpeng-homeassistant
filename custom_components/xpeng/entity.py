"""XpengEntity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
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
        display_name = (
            f"{self.vehicle.information.brand} {self.vehicle.information.model}"
        )
        self._attr_name = f"{display_name} {self.entity_name}"
        self._attr_unique_id = slugify(f"{self.vehicle.id} {self.entity_name}")
        self._attr_device_info = DeviceInfo(
            name=display_name,
            identifiers={(DOMAIN, self.vehicle.id)},
            manufacturer=self.vehicle.information.brand,
            model=self.vehicle.information.model,
            sw_version="",
            serial_number=self.vehicle.information.vin,
        )
        self._last_update_success: bool | None = None
        self.last_update_time: float | None = None

    @property
    def vehicle(self) -> Vehicle:
        """Returns the vehicle data assiciated with this entity."""
        return self.coordinator.data[self._vehicle_id]
