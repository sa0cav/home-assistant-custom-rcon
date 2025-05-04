from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_HOST
from .const import DOMAIN

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    host = config.get(CONF_HOST)
    command = config.get("command", "list")
    scan = config.get("scan_interval", 60)
    add_entities([RconSensor(hass, command)], True)

class RconSensor(Entity):
    def __init__(self, hass, command):
        self._hass = hass
        self._command = command
        self._state = None

    @property
    def name(self):
        return f"RCON: {self._command}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        client = self._hass.data[DOMAIN]["client"]
        self._state = client.command(self._command)
