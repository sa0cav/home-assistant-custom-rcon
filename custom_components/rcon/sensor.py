# custom_components/rcon/sensor.py
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([RconResponseSensor(entry.entry_id)], True)

class RconResponseSensor(Entity):
    def __init__(self, entry_id):
        self._entry_id = entry_id
        self._state = None
        self._attr_unique_id = f"{entry_id}_response"
        self._attr_name = "RCON Response"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._entry_id)}, "name": self._attr_name}

    async def async_added_to_hass(self):
        self.hass.bus.async_listen(f"{DOMAIN}_response", self._handle_event)

    def _handle_event(self, event):
        self._state = event.data.get("response", "")
        self.async_write_ha_state()