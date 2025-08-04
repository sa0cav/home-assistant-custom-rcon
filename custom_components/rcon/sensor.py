# custom_components/rcon/sensor.py

import logging
from datetime import datetime, timedelta
import re

from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)

# A2S fields for common sensors
...

class PlayerCountSensor(Entity):
    """Sensor for the current number of players on the server."""
    def __init__(self, entry_id: str, nickname: str):
        self._attr_name = f"{nickname} Player Count"
        self._attr_unique_id = f"{entry_id}_{nickname}_player_count"
        self._state = None

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        async_track_time_interval(self.hass, self._refresh, SCAN_INTERVAL)

    async def _refresh(self, now: datetime):
        """Fetch the latest player count via A2S or RCON."""
        # implementation...

# ... other sensor classes ...

class RoundNumberSensor(Entity):
    """Sensor for the round number, ignoring warmup rounds."""
    def __init__(self, entry_id: str, nickname: str):
        self._attr_name = f"{nickname} Round Number"
        self._attr_unique_id = f"{entry_id}_{nickname}_round_number"
        self._state = None
        self._started = False  # becomes True after warmup ends

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.hass.bus.async_listen(f"{DOMAIN}_log", self._handle)

    async def _handle(self, event):
        raw = event.data.get("raw", "")

        # 1) When warmup ends or match starts: start counting
        # 3) Count only actual rounds
        if 'Warmup_End' in raw or 'Game_Commencing' in raw:
            self._started = True
            self._round = 0
            self._state = 0
            self.async_write_ha_state()

# ... remaining sensor classes ...

class RawLogSensor(Entity):
    """Sensor for the latest raw log line text (state truncated)."""
    def __init__(self, entry_id: str, nickname: str):
        self._attr_name = f"{nickname} Raw Log"
        self._attr_unique_id = f"{entry_id}_{nickname}_raw_log"
        self._state = None
        self._full_log = ""

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.hass.bus.async_listen(f"{DOMAIN}_log", self._handle)

    async def _handle(self, event):
        raw = event.data.get("raw", "")
        self._full_log = raw
        # Trim state to a maximum of 255 characters
        self._state = raw if len(raw) <= 255 else raw[:252] + "…"
        self.async_write_ha_state()
