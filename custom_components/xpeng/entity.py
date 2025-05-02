"""XpengEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback
from homeassistant.util import slugify

from .enode_models import Vehicle

from .const import DOMAIN
from .coordinator import XpengDataUpdateCoordinator


class XpengEntity(CoordinatorEntity[XpengDataUpdateCoordinator]):
    """XpengEntity class."""

    entity_name = ""

    def __init__(
        self,
        vehicle: Vehicle,
        coordinator: XpengDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        """Initialise the Xpeng car device."""
        self._vehicle = vehicle
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
        # prev_last_update_success = self._last_update_success
        # prev_last_update_time = self.last_update_time
        # coordinator = self.coordinator
        # current_last_update_success = coordinator.last_update_success
        # current_last_update_time = coordinator.last_update_time
        # self._last_update_success = current_last_update_success
        # self.last_update_time = current_last_update_time
        # if (
        #    prev_last_update_success == current_last_update_success
        #    and prev_last_update_time == current_last_update_time
        # ):
        #    # If there was no change in the last update success or time,
        #    # avoid writing state to prevent unnecessary entity updates.
        #    return
        super()._handle_coordinator_update()

    async def update_controller(
        self, *, wake_if_asleep: bool = False, force: bool = True, blocking: bool = True
    ) -> None:
        """Get the latest data from Tesla.

        This does a controller update then a coordinator update.
        The coordinator triggers a call to the refresh function.

        Setting the blocking param to False will create a background task for the update.
        """

        if blocking is False:
            await self.hass.async_create_task(
                self.update_controller(wake_if_asleep=wake_if_asleep, force=force)
            )
            return

        # await self.coordinator.controller.update(
        #    self._car.id, wake_if_asleep=wake_if_asleep, force=force
        # )
        await self.coordinator.async_refresh()
