from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([RconSensor(hass)])

class RconSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._state = None

    @property
    def name(self):
        return "RCON Server Status"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        client: MCRcon = self._hass.data[DOMAIN]["client"]
        # Exempelkommando, t.ex. "list" för Minecraft
        resp = client.command("list")
        self._state = resp
