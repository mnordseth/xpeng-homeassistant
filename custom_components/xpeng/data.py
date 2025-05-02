"""Custom types for xpeng."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import XpengApiClient
    from .coordinator import XpengDataUpdateCoordinator


type XpengConfigEntry = ConfigEntry[XpengData]


@dataclass
class XpengData:
    """Data for the Xpeng integration."""

    client: XpengApiClient
    coordinator: XpengDataUpdateCoordinator
    integration: Integration
